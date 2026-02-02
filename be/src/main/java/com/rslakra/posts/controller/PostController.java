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
package com.rslakra.posts.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.rslakra.posts.domain.Comment;
import com.rslakra.posts.domain.Post;
import com.rslakra.posts.service.PostService;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@RestController
@RequestMapping("${api.version}/posts")
public class PostController {

    private final PostService service;

    /**
     * 
     * @param service
     */
    public PostController(PostService service) {
        this.service = service;
    }

    /**
     * 
     * @return
     */
    @GetMapping
    @ResponseBody
    List<Post> getPosts() {
        return service.getPosts();
    }

    /**
     * 
     * @param id
     * @return
     */
    @GetMapping("/{id}")
    @ResponseBody
    Post getPost(@PathVariable Long id) {
        return service.getPost(id);
    }

    /**
     * 
     * @param post
     * @return
     */
    @PostMapping
    @ResponseBody
    Post create(@RequestBody Post post) {
        return service.create(post);
    }

    /**
     * 
     * @param id
     * @param post
     * @return
     */
    @PutMapping("/{id}")
    @ResponseBody
    Post update(@PathVariable Long id, @RequestBody Post post) {
        return service.update(id, post);
    }

    /**
     * 
     * @param id
     * @return
     */
    @DeleteMapping("/{id}")
    @ResponseBody
    Post delete(@PathVariable Long id) {
        return service.delete(id);
    }

    /**
     * 
     * @param postId
     * @return
     */
    @GetMapping("/{postId}/comments")
    @ResponseBody
    List<Comment> getPostComments(@PathVariable Long postId) {
        return service.getPostComments(postId);
    }

    /**
     * 
     * @param userId
     * @return
     */
    @GetMapping("/?userId={userId}")
    @ResponseBody
    List<Post> getUserPosts(@RequestParam Long userId) {
        return service.getUserPosts(userId);
    }
}
