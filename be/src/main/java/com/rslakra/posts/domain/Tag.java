/*******************************************************************************
 * Copyright (C) Devamatre Inc. 2009-2019. All rights reserved.
 * 
 * This code is licensed to Devamatre under one or more contributor license
 * agreements. The reproduction, transmission or use of this code or the snippet
 * is not permitted without prior express written consent of Devamatre.
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the license is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied and the
 * offenders will be liable for any damages. All rights, including but not
 * limited to rights created by patent grant or registration of a utility model
 * or design, are reserved. Technical specifications and features are binding
 * only insofar as they are specifically and expressly agreed upon in a written
 * contract.
 * 
 * You may obtain a copy of the License for more details at:
 * http://www.devamatre.com/licenses/license.txt.
 * 
 * Devamatre reserves the right to modify the technical specifications and or
 * features without any prior notice.
 *******************************************************************************/
package com.rslakra.posts.domain;

import java.util.HashSet;
import java.util.Set;

import jakarta.persistence.Entity;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@Entity
@Table(name = "tags")
public class Tag extends BaseEntity {

    private String name;

    @ManyToMany(mappedBy = "tags")
    @JsonIgnore
    private Set<Post> posts = new HashSet<>();

    /**
     * Returns the value of the name.
     *
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * The name to be set.
     *
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Returns the value of the posts.
     *
     * @return posts
     */
    public Set<Post> getPosts() {
        return posts;
    }

    /**
     * The posts to be set.
     *
     * @param posts
     */
    public void setPosts(Set<Post> posts) {
        this.posts = posts;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.domain.BaseEntity#toString()
     */
    @Override
    public String toString() {
        return String.format("%s, name=%s", super.toString(), getName());
    }

}
