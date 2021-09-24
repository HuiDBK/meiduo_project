let vm = new Vue({
    el: "#app",

    // 修改Vue读取变量的模板语法
    delimiters: ['[[', ']]'],
    data: {
        // v-model
        username: '',
        password: '',
        confirm_pwd: '',
        mobile: '',
        allow: false,

        // v-show
        error_username: false,
        error_password: false,
        error_confirm_pwd: false,
        error_mobile: false,
        error_allow: false,

        // error_msg
        error_username_msg: '',
        error_mobile_msg: '',

    },

    methods: {
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username_msg = '请输入5-20个字符的用户名';
                this.error_username = true;
            }

            if(this.error_username === false){
                // 判断用户名是否重复注册
                let url = '/usernames/' + this.username + '/count/'
                let options = {responseType: 'json'}
                axios.get(url, options)
                    .then(response => {
                        console.log(response.data)
                        if(response.data.data.count === 1){
                            this.error_username_msg = '用户名已存在';
                            this.error_username = true;
                        }else{
                            this.error_username = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        check_confirm_pwd() {
            if (this.password !== this.confirm_pwd) {
                this.error_confirm_pwd = true;
            } else {
                this.error_confirm_pwd = false;
            }
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;

            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_msg = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },
        check_allow() {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_confirm_pwd();
            this.check_mobile();
            this.check_allow();

            if (this.error_username === true || this.error_password === true || this.error_confirm_pwd === true
                || this.error_mobile === true || this.error_allow === true) {
                // 禁用表单的提交
                window.event.returnValue = false;
                console.log('args error')
            } else {
                console.log('register')
            }
        },
    },


})