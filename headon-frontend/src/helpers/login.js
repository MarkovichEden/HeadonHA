import axios from 'axios';
import Vue from '@/App.vue';
import router from '@/router'

export const loginService = {
    login,
    // logout,
    // update,
};

function login(username, password) {
    const uri = Vue.apiUrl + "/login?username=" + username + "&password=" + password;
    
    axios.get(uri, {
        withCredentials: true
    })
    .then(response => {
        console.log(response)
        var result = response.data
        if (result["success"] == true) {
            localStorage.setItem('username', username)
            localStorage.setItem('token', self.$cookies.get("token"))
            router.push("Dashboard")
        }

        return response;
    })
}