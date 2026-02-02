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

import java.time.Instant;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.rslakra.posts.controller.dto.LoginRequest;
import com.rslakra.posts.controller.dto.RegisterRequest;
import com.rslakra.posts.domain.User;
import com.rslakra.posts.exceptions.RecordUnavailableException;
import com.rslakra.posts.service.UserService;

/**
 * REST controller for authentication: register and login.
 *
 * @author Rohtash Lakra
 * @version 1.0.0
 * @since 1.0.0
 */
@RestController
@RequestMapping("${api.version}/auth")
public class AuthController {

    private static final String DEFAULT_STATUS = "ACTIVE";
    private static final String DEFAULT_ROLE = "ROLE_USER";

    private final UserService userService;
    private final PasswordEncoder passwordEncoder;

    /**
     * @param userService      the user service
     * @param passwordEncoder   the password encoder (BCrypt)
     */
    public AuthController(UserService userService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * Registers a new user and returns the created user (logged-in state).
     *
     * @param request registration data (email, password, firstName, middleName, lastName)
     * @return the created user
     */
    @PostMapping("/register")
    @ResponseBody
    public ResponseEntity<User> register(@RequestBody RegisterRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setFirstName(request.getFirstName());
        user.setMiddleName(request.getMiddleName());
        user.setLastName(request.getLastName());
        user.setStatus(DEFAULT_STATUS);
        user.setRoles(DEFAULT_ROLE);

        long now = System.currentTimeMillis();
        Instant instant = Instant.now();
        String principal = request.getEmail();

        user.setCreatedOn(now);
        user.setCreatedAt(instant);
        user.setCreatedBy(principal);
        user.setUpdatedOn(now);
        user.setUpdatedAt(instant);
        user.setUpdatedBy(principal);

        user = userService.create(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    /**
     * Logs in a user by email and password. Returns the user if credentials are valid.
     *
     * @param request login data (email, password)
     * @return the user if authenticated, or 401 Unauthorized
     */
    @PostMapping("/login")
    @ResponseBody
    public ResponseEntity<User> login(@RequestBody LoginRequest request) {
        try {
            User user = userService.getUserByEmail(request.getEmail());
            if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
            }
            return ResponseEntity.ok(user);
        } catch (RecordUnavailableException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }
}
