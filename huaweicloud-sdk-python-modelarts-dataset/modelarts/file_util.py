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

from modelarts.field_name import prefix_s3, prefix_s3_upper, s3, separator
from obs import *


def __is_local(path):
  """
  return whether is local path
  TODO: enhance it
  :param path: file path
  :return: true if the path is local path, false if the path isn't local path
  """
  if path is None:
    raise ValueError('path is None')
  if str(path).lower().startswith("s3") or str(path).startswith("hdfs"):
    return False
  return True


def __parser_path(path):
  """
  parser the path and return bucket_name and file_name
  :param path: the file path
  :return: bucket_name and file_name
  """
  base_url = str(path)[len(prefix_s3):] or str(path)[len(prefix_s3_upper):]
  split_array = base_url.split(separator)
  bucket_name = split_array[0]
  file_name = separator.join(split_array[1:])
  return bucket_name, file_name


def __read(path, access_key, secret_key, end_point):
  """
  read data from OBS and return the binary of file
  :param path: the file path
  :param access_key: access key of OBS
  :param secret_key: secret key of OBS
  :param end_point: end point of OBS
  :return: result buffer
  """
  if str(path).lower().startswith(s3):
    obs_client = ObsClient(
      access_key_id=access_key,
      secret_access_key=secret_key,
      server=end_point,
      long_conn_mode=True
    )
    bucket_name, file = __parser_path(path)

    resp = obs_client.getObject(bucket_name, file, loadStreamInMemory=True)
    if resp.body is None:
      resp = obs_client.getObject(bucket_name, file, loadStreamInMemory=True)
    if resp.body is None:
      raise Exception("Failed,status: " + str(resp.status) + ", errorCode: " + str(resp.errorCode)
                      + ", errorMessage: " + resp.errorMessage + " reason: " + resp.reason)
    return resp.body.buffer
  else:
    raise ValueError("Only support s3 now!")


def save(manifest_json, path, access_key, secret_key, end_point):
  """
  read data from OBS and return the binary of file
  :param manifest_json: manifest json list
  :param path: the file path
  :param access_key: access key of OBS
  :param secret_key: secret key of OBS
  :param end_point: end point of OBS
  :return:
  """
  if str(path).lower().startswith(s3):
    obs_client = ObsClient(
      access_key_id=access_key,
      secret_access_key=secret_key,
      server=end_point,
      long_conn_mode=True
    )
    bucket_name, file = __parser_path(path)
    content = AppendObjectContent()

    resp = obs_client.getObjectMetadata(bucket_name, file)
    if resp.status < 300:
      content.position = resp.body.nextPosition
    for line in manifest_json:
      content.content = line + "\n"
      resp = obs_client.appendObject(bucket_name, file, content=content)
      if resp.body is None:
        resp = obs_client.appendObject(bucket_name, file, content=content)
      if resp.body is None:
        raise Exception("Failed,status: " + str(resp.status) + ", errorCode: " + str(resp.errorCode)
                        + ", errorMessage: " + resp.errorMessage + " reason: " + resp.reason)
      content.position = resp.body.nextPosition
    return resp.body.buffer
  else:
    raise ValueError("Only support s3 now!")
