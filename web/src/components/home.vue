<!-- https://axios-http.com/docs/post_example -->

<template>
  <div style="margin: 0 0 2rem 0; padding: 1rem; background: #1d1d1d;">
    <p>{{ msg }} <b style="color:#9981b4;">V případě chyby ve výsledku prosím o přiložení hash.</b></p>
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
          this.msg = res.data;
        })
        .catch((error) => {
          this.msg = "Nelze se připojit k serveru. Interní chyba: " + error.code + "."
          console.error(error);
        });
    },
    change() {
      this.optional = !this.optional
      console.log(this.optional)
    }
  },
  created() {
    this.getMessage();
  },
};
</script>