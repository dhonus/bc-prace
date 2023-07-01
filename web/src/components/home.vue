<!-- https://axios-http.com/docs/post_example -->

<template>
  <div v-if="msg" class="noprint" style="padding: 0 0 2rem 0;">
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping-me',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      axios.get('/')
        .then((res) => {
          //this.msg = res.data;
        })
        .catch((error) => {
          this.msg = "Nelze se připojit k serveru. Interní chyba: " + error.code + "."
          console.error(error);
        });
    },
    change() {
      this.optional = !this.optional
    }
  },
  created() {
    this.getMessage();
  },
};
</script>