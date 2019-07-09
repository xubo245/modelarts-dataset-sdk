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

package com.huaweicloud.modelarts.dataset.format.voc;

public class Source
{
    private String database;
    
    private String annotation;
    
    private String image;
    
    public Source(String database)
    {
        this.database = database;
    }
    
    public Source(String database, String annotation, String image)
    {
        this.database = database;
        this.annotation = annotation;
        this.image = image;
    }
    
    public void setDatabase(String database)
    {
        this.database = database;
    }
    
    public void setAnnotation(String annotation)
    {
        this.annotation = annotation;
    }
    
    public void setImage(String image)
    {
        this.image = image;
    }
    
    public String getDatabase()
    {
        return database;
    }
    
    public String getAnnotation()
    {
        return annotation;
    }
    
    public String getImage()
    {
        return image;
    }
}
