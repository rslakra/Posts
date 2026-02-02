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
import java.util.Optional;

import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import com.rslakra.posts.domain.Comment;
import com.rslakra.posts.domain.Post;
import com.rslakra.posts.exceptions.RecordUnavailableException;
import com.rslakra.posts.repository.CommentRepository;
import com.rslakra.posts.repository.PostRepository;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@Service
public class PostServiceImpl implements PostService {

    private final PostRepository repository;
    private final CommentRepository commentRepository;

    /**
     * 
     * @param repository
     */
    public PostServiceImpl(PostRepository repository, CommentRepository commentRepository) {
        this.repository = repository;
        this.commentRepository = commentRepository;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#getPosts()
     */
    @Override
    public List<Post> getPosts() {
        return repository.findAll();
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#getPost(java.lang.Long)
     */
    @Override
    public Post getPost(Long id) {
        Optional<Post> post = repository.findById(id);
        if (post.isPresent()) {
            return post.get();
        }

        throw new RecordUnavailableException("No Record found for id:" + id);
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#create(com.rslakra.posts.domain.Post)
     */
    @Override
    public Post create(Post post) {
        post = repository.saveAndFlush(post);
        return post;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#update(java.lang.Long,
     *      com.rslakra.posts.domain.Post)
     */
    @Override
    public Post update(Long id, Post post) {
        Post oldPost = repository.findById(id)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for id:" + id));
        BeanUtils.copyProperties(post, oldPost);
        repository.saveAndFlush(oldPost);
        return oldPost;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#delete(java.lang.Long)
     */
    @Override
    public Post delete(Long id) {
        Post post = repository.findById(id)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for id:" + id));
        repository.deleteById(id);
        return post;
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#getComments(java.lang.Long)
     */
    @Override
    public List<Comment> getPostComments(Long postId) {
        return commentRepository.findCommentsByPostId(postId);
    }

    /**
     * (non-Javadoc)
     * 
     * @see com.rslakra.posts.service.PostService#getUserPosts(java.lang.Long)
     */
    @Override
    public List<Post> getUserPosts(Long userId) {
        return null;
    }

}
