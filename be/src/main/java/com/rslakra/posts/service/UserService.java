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

import com.rslakra.posts.domain.User;

/**
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
public interface UserService {

    /**
     * Returns all users.
     *
     * @return list of users
     */
    List<User> getUsers();

    /**
     * Returns the user for the given id.
     *
     * @param id the user id
     * @return the user
     */
    User getUser(Long id);

    /**
     * Returns the user for the given email.
     *
     * @param email the email
     * @return the user if found
     */
    User getUserByEmail(String email);

    /**
     * Creates a new user.
     *
     * @param user the user to create
     * @return the created user
     */
    User create(User user);

    /**
     * Updates the user for the given id.
     *
     * @param id   the user id
     * @param user the updated user data
     * @return the updated user
     */
    User update(Long id, User user);

    /**
     * Deletes the user for the given id.
     *
     * @param id the user id
     * @return the deleted user
     */
    User delete(Long id);
}
