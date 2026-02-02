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

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@Entity
@Table(name = "posts")
public class Post extends BaseEntity {

    private String title;

    @OneToOne(optional = false, orphanRemoval = true, cascade = CascadeType.ALL, fetch = FetchType.LAZY, mappedBy = "post")
    private PostDetail postDetail;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "post_id")
    private List<Comment> comments = new ArrayList<>();

    @ManyToMany
    @JoinTable(name = "posts_tags", joinColumns = @JoinColumn(name = "post_id"), inverseJoinColumns = @JoinColumn(name = "tag_id"))
    private List<Tag> tags = new ArrayList<>();

    /**
     * Returns the value of the title.
     *
     * @return title
     */
    public String getTitle() {
        return title;
    }

    /**
     * The title to be set.
     *
     * @param title
     */
    public void setTitle(String title) {
        this.title = title;
    }

    /**
     * Returns the value of the postDetail.
     *
     * @return postDetail
     */
    public PostDetail getPostDetail() {
        return postDetail;
    }

    /**
     * The postDetail to be set.
     *
     * @param postDetail
     */
    public void setPostDetail(PostDetail postDetail) {
        if (postDetail == null) {
            if (this.postDetail != null) {
                this.postDetail.setPost(null);
            }
        } else {
            postDetail.setPost(this);
        }
        this.postDetail = postDetail;
    }

    /**
     * Returns the value of the comments.
     *
     * @return comments
     */
    public List<Comment> getComments() {
        return comments;
    }

    /**
     * The comments to be set.
     *
     * @param comments
     */
    public void setComments(List<Comment> comments) {
        this.comments = comments;
    }

    /**
     * Returns the value of the tags.
     *
     * @return tags
     */
    public List<Tag> getTags() {
        return tags;
    }

    /**
     * The tags to be set.
     *
     * @param tags
     */
    public void setTags(List<Tag> tags) {
        this.tags = tags;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.domain.BaseEntity#toString()
     */
    @Override
    public String toString() {
        return String.format("%s, title=%s, postDetail=%s, comments=%s, tags=%s", super.toString(), getTitle(),
                getPostDetail(), getComments(), getTags());
    }

}
