/*
 * Copyright 2018 Deep Learning Service of Huawei Cloud. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.huaweicloud.modelarts.dataset;

import java.util.ArrayList;
import java.util.List;

/**
 * Dataset class for manifest
 */
public class Dataset {
  /**
   * the number of sample in manifest/dataset
   */
  private int size;

  /**
   * sample list in manifest/dataset
   */
  private List<Sample> samples;

  public Dataset() {
    samples = new ArrayList<Sample>();
  }

  public Dataset(List<Sample> samples) {
    this.samples = samples;
  }

  public Dataset(int size, List<Sample> samples) {
    this.size = size;
    this.samples = samples;
  }

  public int getSize() {
    return size;
  }

  public void setSize(int size) {
    this.size = size;
  }

  public List<Sample> getSamples() {
    return samples;
  }

  public void setSamples(List<Sample> samples) {
    this.samples = samples;
  }

  /**
   * Add a sample into dataset object
   *
   * @param sample sample of manifest
   */
  public void addSample(Sample sample) {
    this.samples.add(sample);
  }
}
