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

import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import com.rslakra.posts.domain.User;
import com.rslakra.posts.exceptions.RecordUnavailableException;
import com.rslakra.posts.repository.UserRepository;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository repository;

    /**
     * @param repository the user repository
     */
    public UserServiceImpl(UserRepository repository) {
        this.repository = repository;
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#getUsers()
     */
    @Override
    public List<User> getUsers() {
        return repository.findAll();
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#getUser(java.lang.Long)
     */
    @Override
    public User getUser(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for id:" + id));
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#getUserByEmail(java.lang.String)
     */
    @Override
    public User getUserByEmail(String email) {
        return repository.findByEmail(email)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for email:" + email));
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#create(com.rslakra.posts.domain.User)
     */
    @Override
    public User create(User user) {
        return repository.saveAndFlush(user);
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#update(java.lang.Long,
     *      com.rslakra.posts.domain.User)
     */
    @Override
    public User update(Long id, User user) {
        User existing = repository.findById(id)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for id:" + id));
        BeanUtils.copyProperties(user, existing, "id");
        return repository.saveAndFlush(existing);
    }

    /**
     * (non-Javadoc)
     *
     * @see com.rslakra.posts.service.UserService#delete(java.lang.Long)
     */
    @Override
    public User delete(Long id) {
        User user = repository.findById(id)
                .orElseThrow(() -> new RecordUnavailableException("No Record found for id:" + id));
        repository.deleteById(id);
        return user;
    }
}
