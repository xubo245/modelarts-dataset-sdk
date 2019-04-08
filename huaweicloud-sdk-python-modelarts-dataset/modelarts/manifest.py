# Copyright 2018 Deep Learning Service of Huawei Cloud. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json

from modelarts import field_name
from modelarts.file_util import __is_local, save
from modelarts.file_util import __read


def get_sample_list(manifest_path, task_type, exactly_match_type=False, access_key=None,
                    secret_key=None, end_point=None, usage=field_name.default_usage):
  """
  get the sample list from manifest, support local and OBS path;
  If the exactly_match_type is True, then it will match the task type exactly;
  If the exactly_match_type is False, then it will not match the task type exactly and match the suffix of the type
  default_usage is all. Users can use usage="train" if users want to get train sample.
  default task type is all.

  :param manifest_path:  manifest file path
  :param task_type:  task type, like: image_classification, object_detection
  :param exactly_match_type: whether exactly match task type. Users can set True if users want to match exactly,
        like "modelarts/image_classification; Users can set False if users don't want to match exactly,
        like "image_classification;
  :param access_key: access key of OBS
  :param secret_key: secret key of OBS
  :param end_point: end point of OBS
  :param usage: usage of the sample, like "TRAIN", "EVAL", "TEST", "inference", "all", default value is all
  :return: data_list, label_type
  """
  data_set = parse_manifest(manifest_path, access_key=access_key, secret_key=secret_key, end_point=end_point)
  sample_list = data_set.get_sample_list()
  data_list = []
  label_type = field_name.single_lable
  for sample in sample_list:
    annotations = sample.get_annotations()
    sample_usage = sample.get_usage()
    if str(sample_usage).lower().__eq__(str(usage).lower()) or str(usage).lower().__eq__(field_name.default_usage):
      label_list = []
      i = 0
      for annotation in annotations:
        if i > 0:
          label_type = field_name.multi_lable
        i = i + 1
        type = annotation.get_type()
        if not exactly_match_type:
          if str(type).endswith("/" + task_type):
            if (task_type == field_name.image_classification or task_type == field_name.sound_classification
                    or task_type == field_name.text_classification):
              label_list.append(annotation.get_name())
            if task_type == field_name.object_detection:
              label_list.append(annotation.get_loc())

        elif exactly_match_type:
          if type == task_type:
            if str(task_type).endswith("/" + field_name.image_classification) \
                    or str(task_type).endswith("/" + field_name.sound_classification) \
                    or str(task_type).endswith("/" + field_name.text_classification):
              label_list.append(annotation.get_name())
            if str(task_type).endswith("/" + field_name.object_detection):
              label_list.append(annotation.get_loc())
    else:
      continue
    data_list.append([sample.get_source(), label_list])
  return data_list, label_type


def parse_manifest(manifest_path, access_key=None, secret_key=None, end_point=None):
  """
  user give the path of manifest file, it will return the dataset,
  including data object list, annotation list and so on after the manifest was parsed.

  :param manifest_path:  path of manifest file
  :param access_key: access key of OBS
  :param secret_key: secret key of OBS
  :param end_point: end point of OBS
  :return: data set of manifest
  """

  def __getDataSet(lines):
    sample_list = []
    size = 0
    for line in lines:
      if line != '':
        size = size + 1
        text = json.loads(line)
        source = text.get(field_name.source)
        assert source is not None
        usage = text.get(field_name.usage)
        id = text.get(field_name.id)
        annotations = text.get(field_name.annotation)
        inference_loc = text.get(field_name.inference_loc) or text.get(field_name.inference_loc2)
        annotations_list = []
        if annotations is not None:
          for annotation in annotations:
            annotation_type = annotation.get(field_name.annotation_type)
            annotation_name = annotation.get(field_name.annotation_name)
            annotation_loc = annotation.get(field_name.annotation_loc) or annotation.get(field_name.annotation_loc2)
            annotation_creation_time = annotation.get(field_name.annotation_creation_time) or annotation.get(
              field_name.annotation_creation_time2)
            annotation_property = annotation.get(field_name.annotation_property)
            annotation_format = annotation.get(field_name.annotation_format) or annotation.get(
              field_name.annotation_format2)
            annotation_confidence = annotation.get(field_name.annotation_confidence)
            annotated_by = annotation.get(field_name.annotation_annotated_by) or annotation.get(
              field_name.annotation_annotated_by2)
            annotations_list.append(
              Annotation(name=annotation_name, type=annotation_type, loc=annotation_loc,
                         property=annotation_property,
                         confidence=annotation_confidence,
                         creation_time=annotation_creation_time,
                         annotated_by=annotated_by, annotation_format=annotation_format))
        sample_list.append(
          Sample(source=source, usage=usage, annotations=annotations_list, inference_loc=inference_loc, id=id))
    return DataSet(sample=sample_list, size=size)

  local = __is_local(manifest_path)

  if local:
    with open(manifest_path) as f_obj:
      lines = f_obj.readlines()
      return __getDataSet(lines)
  else:
    if access_key is None or secret_key is None or end_point is None:
      raise ValueError("Please input ak, sk and endpoint")
    data = __read(manifest_path, access_key=access_key, secret_key=secret_key, end_point=end_point)
    result = __getDataSet(data.decode().split("\n"))
    return result


class DataSet(object):
  """
  dataset for manifest
  dataset architecture:
    --size
    --sample list
      --sample 1
      --sample 2
          --source
          ...
          --annotation list
            --annotation 1
            --annotation 2
              --name
              --annotation_loc
              --type
              ...
              annotated_by
  """

  def __init__(self, sample, size=None):
    self.__sample = sample
    self.__size = size

  def get_size(self):
    """
    :return size of the data set
    Optional field
    """
    return self.__size

  def get_sample_list(self):
    """
    :return a list of sample
    Mandatory field
    """
    return self.__sample

  def __put(self, sample_json, key, value):
    """
    put key and value to sample_json if value is not None
    :param sample_json: sample json
    :param key: key
    :param value: value
    :return: sample json
    """
    if value is not None:
      sample_json[key] = value
    return sample_json

  def __annotations_to_json(self, annotations):
    """
    convert annotations to json
    :return annotation json
    """
    annotations_json = []
    annotation_json = {}
    if annotations is None:
      return None
    for annotation in annotations:
      self.__put(annotation_json, field_name.annotation_name, annotation.get_name())
      self.__put(annotation_json, field_name.annotation_loc, annotation.get_loc())
      self.__put(annotation_json, field_name.annotation_type, annotation.get_type())
      self.__put(annotation_json, field_name.annotation_confidence, annotation.get_confidence())
      self.__put(annotation_json, field_name.annotation_property, annotation.get_property())
      self.__put(annotation_json, field_name.annotation_hard, annotation.get_hard())
      self.__put(annotation_json, field_name.annotation_annotated_by, annotation.get_annotated_by())
      self.__put(annotation_json, field_name.annotation_creation_time, annotation.get_creation_time())
      self.__put(annotation_json, field_name.annotation_format, annotation.get_annotation_format())
      annotations_json.append(annotation_json)
    return annotations_json

  def __toJSON(self, sample):
    """
    convert sample to json
    :param sample: sample object of dataset
    :return: sample json
    """
    sample_json = {}
    self.__put(sample_json, field_name.id, sample.get_id())
    self.__put(sample_json, field_name.source, sample.get_source())
    self.__put(sample_json, field_name.usage, sample.get_usage())
    self.__put(sample_json, field_name.inference_loc, sample.get_inference_loc())
    self.__put(sample_json, field_name.annotation, self.__annotations_to_json(sample.get_annotations()))
    return sample_json;

  def save(self, path, *args):
    """
    save dataset to local or OBS
    :param path: manifest output path
    :param args: ak,sk,endpoint
    :return: None
    """
    if args.__len__() < 1:
      for sample in self.get_sample_list():
        with open(path, "a") as f_obj:
          value = self.__toJSON(sample);
          json.dump(value, f_obj)
          f_obj.write('\n')
    else:
      if (args.__len__() < 3):
        raise ValueError("please input OBS path, ak, sk and endpoint.")
      manifest_json = []
      for sample in self.get_sample_list():
        value = self.__toJSON(sample);
        manifest_json.append(json.dumps(value))
      save(manifest_json, path, args[0], args[1], args[2])


class Sample(object):
  def __init__(self, source, annotations=None, usage=None, inference_loc=None, id=None):
    self.__source = source
    self.__usage = usage
    self.__annotation = annotations
    self.__inference_loc = inference_loc
    self.__id = id

  def get_source(self):
    """
    :return "source" attribute
    Mandatory field
    """
    return self.__source

  def get_id(self):
    """
    :return "id" attribute, one of
    Optional field
    """
    return self.__id

  def get_usage(self):
    """
    :return "usage" attribute, one of
    Optional field
    """
    return self.__usage

  def get_inference_loc(self):
    """
    :return "inference_loc" attribute, one of Optional field
    """
    return self.__inference_loc

  def get_annotations(self):
    """
    :return a list of class Annotation
    Optional field
    """
    return self.__annotation


class Annotation:

  def __init__(self, name=None, type=None, loc=None, property=None, confidence=None, creation_time=None,
               annotated_by=None, annotation_format=None, hard=None):
    self.__name = name
    self.__type = type
    self.__annotation_loc = loc
    self.__property = property
    self.__hard = hard
    self.__confidence = confidence
    self.__creation_time = creation_time
    self.__annotated_by = annotated_by
    self.__annotation_format = annotation_format

  def get_type(self):
    """
    :return type of dataset: modelarts/image_classification, modelarts/object_detection
    Optional field
    """
    return self.__type

  def get_name(self):
    """
    :return the name of this annotation, like "cat"
    Mandatory field if get_loc is None
    """
    return self.__name

  def get_loc(self):
    """
    :return in case of object detection, this will return the annotation file,
    otherwise return null
    Mandatory field if get_name is None
    """
    return self.__annotation_loc

  def get_property(self):
    """
    :return a KV pair list
    Optional field
    """
    return self.__property

  def get_hard(self):
    """
    :return set true if it's hard annotation, set false  if it's not hard annotation
    Optional field
    """
    return self.__hard

  def get_confidence(self):
    """
    :return confidence of label
    Optional field
    """
    return self.__confidence

  def get_creation_time(self):
    """
    :return when this annotation is created
    Optional field
    """
    return self.__creation_time

  def get_annotation_format(self):
    """
    :return when this annotation format
    Optional field
    """
    return self.__annotation_format

  def get_annotated_by(self):
    """
    :return who this annotation is created by
    Optional field
    """
    return self.__annotated_by
