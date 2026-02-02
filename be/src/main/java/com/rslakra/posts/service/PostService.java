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
package com.rslakra.posts.service;

import java.util.List;

import com.rslakra.posts.domain.Comment;
import com.rslakra.posts.domain.Post;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
public interface PostService {

    /**
     * 
     * @return
     */
    List<Post> getPosts();

    /**
     * 
     * @param id
     * @return
     */
    Post getPost(Long id);

    /**
     * 
     * @param post
     * @return
     */
    Post create(Post post);

    /**
     * 
     * @param id
     * @param post
     * @return
     */
    Post update(Long id, Post post);

    /**
     * 
     * @param id
     * @return
     */
    Post delete(Long id);

    /**
     * 
     * @param postId
     * @return
     */
    List<Comment> getPostComments(Long postId);

    /**
     * 
     * @param userId
     * @return
     */
    List<Post> getUserPosts(Long userId);

}
