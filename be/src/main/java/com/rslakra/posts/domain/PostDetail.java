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

import java.util.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.MapsId;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@Entity
@Table(name = "post_details")
public class PostDetail {

    @Id
    private Long id;

    private String description;

    @Column(name = "created_on")
    private Date createdOn;

    @Column(name = "created_by")
    private String createdBy;

    @MapsId
    @JoinColumn(name = "id")
    @OneToOne(optional = false, fetch = FetchType.LAZY)
    @JsonIgnore
    private Post post;

    PostDetail() {
        createdOn = new Date();
        createdBy = "Rohtash Lakra";
    }

    /**
     * Returns the value of the id.
     *
     * @return id
     */
    public Long getId() {
        return id;
    }

    /**
     * The id to be set.
     *
     * @param id
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * Returns the value of the description.
     *
     * @return description
     */
    public String getDescription() {
        return description;
    }

    /**
     * The description to be set.
     *
     * @param description
     */
    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * Returns the value of the createdOn.
     *
     * @return createdOn
     */
    public Date getCreatedOn() {
        return createdOn;
    }

    /**
     * The createdOn to be set.
     *
     * @param createdOn
     */
    public void setCreatedOn(Date createdOn) {
        this.createdOn = createdOn;
    }

    /**
     * Returns the value of the createdBy.
     *
     * @return createdBy
     */
    public String getCreatedBy() {
        return createdBy;
    }

    /**
     * The createdBy to be set.
     *
     * @param createdBy
     */
    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    /**
     * Returns the value of the post.
     *
     * @return post
     */
    public Post getPost() {
        return post;
    }

    /**
     * 
     * @param post
     */
    public void setPost(Post post) {
        this.post = post;
    }

    /**
     * (non-Javadoc)
     * 
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return String.format("%s, description=%s, createdOn=%s, createdBy=%s", super.toString(), getDescription(),
                getCreatedOn(), getCreatedBy());
    }

}
