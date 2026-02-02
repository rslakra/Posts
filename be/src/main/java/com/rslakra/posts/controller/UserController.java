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

import com.rslakra.posts.domain.User;
import com.rslakra.posts.service.UserService;

/**
 * REST controller for User resources.
 *
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@RestController
@RequestMapping("${api.version}/users")
public class UserController {

    private final UserService service;

    /**
     * @param service the user service
     */
    public UserController(UserService service) {
        this.service = service;
    }

    /**
     * Returns all users.
     *
     * @return list of users
     */
    @GetMapping
    @ResponseBody
    List<User> getUsers() {
        return service.getUsers();
    }

    /**
     * Returns the user for the given id.
     *
     * @param id the user id
     * @return the user
     */
    @GetMapping("/{id}")
    @ResponseBody
    User getUser(@PathVariable Long id) {
        return service.getUser(id);
    }

    /**
     * Returns the user for the given email.
     *
     * @param email the email
     * @return the user
     */
    @GetMapping(params = "email")
    @ResponseBody
    User getUserByEmail(@RequestParam String email) {
        return service.getUserByEmail(email);
    }

    /**
     * Creates a new user.
     *
     * @param user the user to create
     * @return the created user
     */
    @PostMapping
    @ResponseBody
    User create(@RequestBody User user) {
        return service.create(user);
    }

    /**
     * Updates the user for the given id.
     *
     * @param id   the user id
     * @param user the updated user data
     * @return the updated user
     */
    @PutMapping("/{id}")
    @ResponseBody
    User update(@PathVariable Long id, @RequestBody User user) {
        return service.update(id, user);
    }

    /**
     * Deletes the user for the given id.
     *
     * @param id the user id
     * @return the deleted user
     */
    @DeleteMapping("/{id}")
    @ResponseBody
    User delete(@PathVariable Long id) {
        return service.delete(id);
    }
}
