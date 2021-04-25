<template>
  <v-container>
      <v-form ref="form" v-model="valid" lazy-validation method="get">
          <v-text-field
            v-model="username"
            :rules="nameRules"
            label="User Name"
            required
            ></v-text-field>
            <v-text-field
            v-model="password"
            :rules="passwordRules"
            label="Password"
            required
            type="password"
        ></v-text-field>
        <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="validate"
        >
        Login
        </v-btn>

        <v-btn
            color="error"
            class="mr-4"
            @click="reset"
        >
        Reset
        </v-btn>

        <v-btn
            color="warning"
            @click="resetValidation"
        >
        Reset Validation
        </v-btn>
      </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';
import {loginService} from '../helpers'

export default {
    name: 'LoginComponent',
    data: () => ({
        valid: false,
        username: '',
        nameRules: [
            v => !!v || 'User name is required',
        ],
        password: '',
        passwordRules: [
            v => !!v || 'Password is required',
        ],
    }),

    methods: {
        validate() {
            if (this.nameRules[0](this.username) && this.passwordRules[0](this.password)) {
                loginService.login(this.username, this.password)
            } else {
                alert("invalid")
            }
        },
        reset() {
            this.$refs.form.reset()
        },
        resetValidation() {
            this.$refs.form.resetValidation()
        }
    }
}
</script>

<style>

</style>