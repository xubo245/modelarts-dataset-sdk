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

public class Annotation {
  private String name;
  private String type;
  private String annotationLoc;
  private String property;
  private double confidence;
  private String creation_time;
  private String annotated_by;
  private String annotation_format;

  public Annotation() {
  }

  public Annotation(String name) {
    this.name = name;
  }

  public Annotation(String name, String type, String annotationLoc, String property, double confidence, String creation_time, String annotated_by, String annotation_format) {
    this.name = name;
    this.type = type;
    this.annotationLoc = annotationLoc;
    this.property = property;
    this.confidence = confidence;
    this.creation_time = creation_time;
    this.annotated_by = annotated_by;
    this.annotation_format = annotation_format;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getannotationLoc() {
    return annotationLoc;
  }

  public void setannotationLoc(String annotationLoc) {
    this.annotationLoc = annotationLoc;
  }

  public String getProperty() {
    return property;
  }

  public void setProperty(String property) {
    this.property = property;
  }

  public double getConfidence() {
    return confidence;
  }

  public void setConfidence(double confidence) {
    this.confidence = confidence;
  }

  public String getCreation_time() {
    return creation_time;
  }

  public void setCreation_time(String creation_time) {
    this.creation_time = creation_time;
  }

  public String getAnnotated_by() {
    return annotated_by;
  }

  public void setAnnotated_by(String annotated_by) {
    this.annotated_by = annotated_by;
  }

  public String getAnnotation_format() {
    return annotation_format;
  }

  public void setAnnotation_format(String annotation_format) {
    this.annotation_format = annotation_format;
  }
}
