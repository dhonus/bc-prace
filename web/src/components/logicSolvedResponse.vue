<!-- https://axios-http.com/docs/post_example -->

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