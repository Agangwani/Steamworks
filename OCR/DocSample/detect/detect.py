#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.

Example Usage:
python detect.py text ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py web-geo ./resources/city.jpg
python detect.py faces-uri gs://your-bucket/file.jpg
python detect.py ocr-uri gs://python-docs-samples-tests/HodgeConj.pdf \
gs://BUCKET_NAME/PREFIX/
python detect.py object-localization ./resources/puppies.jpg
python detect.py object-localization-uri gs://...

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io
import re

# [START vision_text_detection]
def detect_text(path):
    detectFILE= open("speechfile.txt", "a")
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        text = str(text.description)
        detectFILE.write(text)
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    detectFILE.close()
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]


# [START vision_text_detection_gcs]
def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
# [END vision_text_detection_gcs]


# [START vision_image_property_detection]
def detect_properties(path):
    """Detects image properties in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_image_properties]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
    # [END vision_python_migration_image_properties]
# [END vision_image_property_detection]


# [START vision_image_property_detection_gcs]
def detect_properties_uri(uri):
    """Detects image properties in the file located in Google Cloud Storage or
    on the Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('frac: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
# [END vision_image_property_detection_gcs]



# [START vision_text_detection_pdf_gcs]
def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    from google.cloud import vision
    from google.cloud import storage
    from google.protobuf import json_format
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name=bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())

    # The actual response for the first page of the input file.
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print(u'Full text:\n{}'.format(
        annotation.text))
# [END vision_text_detection_pdf_gcs]


# [START vision_localize_objects]
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
# [END vision_localize_objects]


# [START vision_localize_objects_gcs]
def localize_objects_uri(uri):
    """Localize objects in the image on Google Cloud Storage

    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image()
    image.source.image_uri = uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
# [END vision_localize_objects_gcs]


def run_local(args):
    if args.command == 'faces':
        detect_faces(args.path)
    elif args.command == 'labels':
        detect_labels(args.path)
    elif args.command == 'landmarks':
        detect_landmarks(args.path)
    elif args.command == 'text':
        detect_text(args.path)
    elif args.command == 'logos':
        detect_logos(args.path)
    elif args.command == 'safe-search':
        detect_safe_search(args.path)
    elif args.command == 'properties':
        detect_properties(args.path)
    elif args.command == 'web':
        detect_web(args.path)
    elif args.command == 'crophints':
        detect_crop_hints(args.path)
    elif args.command == 'document':
        detect_document(args.path)
    elif args.command == 'web-geo':
        web_entities_include_geo_results(args.path)
    elif args.command == 'object-localization':
        localize_objects(args.path)


def run_uri(args):
    if args.command == 'text-uri':
        detect_text_uri(args.uri)
    elif args.command == 'faces-uri':
        detect_faces_uri(args.uri)
    elif args.command == 'labels-uri':
        detect_labels_uri(args.uri)
    elif args.command == 'landmarks-uri':
        detect_landmarks_uri(args.uri)
    elif args.command == 'logos-uri':
        detect_logos_uri(args.uri)
    elif args.command == 'safe-search-uri':
        detect_safe_search_uri(args.uri)
    elif args.command == 'properties-uri':
        detect_properties_uri(args.uri)
    elif args.command == 'web-uri':
        detect_web_uri(args.uri)
    elif args.command == 'crophints-uri':
        detect_crop_hints_uri(args.uri)
    elif args.command == 'document-uri':
        detect_document_uri(args.uri)
    elif args.command == 'web-geo-uri':
        web_entities_include_geo_results_uri(args.uri)
    elif args.command == 'ocr-uri':
        async_detect_document(args.uri, args.destination_uri)
    elif args.command == 'object-localization-uri':
        localize_objects_uri(args.uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    text_file_parser = subparsers.add_parser(
        'text-uri', help=detect_text_uri.__doc__)
    text_file_parser.add_argument('uri')

    
    ocr_uri_parser = subparsers.add_parser(
        'ocr-uri', help=async_detect_document.__doc__)
    ocr_uri_parser.add_argument('uri')
    ocr_uri_parser.add_argument('destination_uri')

    object_localization_parser = subparsers.add_parser(
        'object-localization', help=async_detect_document.__doc__)
    object_localization_parser.add_argument('path')

    object_localization_uri_parser = subparsers.add_parser(
        'object-localization-uri', help=async_detect_document.__doc__)
    object_localization_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)
