<template>
  <app-page title="Настройки пользователя">
    <h2>Логин: {{username}}</h2>
    <h2 style="margin-right: 10px;">Телефон: {{phone}}</h2>
    <h2 style="margin-right: 10px;">Имя: {{firstname}}</h2>
    <h2 style="margin-right: 10px;">Фамилия: {{lastname}}</h2>
    <h2>Баланс: {{balance}} руб.</h2>
  </app-page>
</template>

<script>
import AppPage from "@/components/ui/AppPage";
import {useStore} from "vuex";
import axios from "axios";
import {ref} from "vue";

export default {
  setup() {
    const store = useStore()
    const username = ref(null)
    const phone = ref(null)
    const password = ref(null)
    const firstname = ref(null)
    const lastname = ref(null)
    const balance = ref(null)

    const getUser = async () => {
      const data = await axios.get('http://127.0.0.1:8000/api/users/', {
        params: {
          username: store.getters['auth/username']
        }
      })

      username.value = data.data[0].username
      phone.value = data.data[0].phone
      password.value = data.data[0].password
      firstname.value = data.data[0].first_name
      lastname.value = data.data[0].last_name
      balance.value = data.data[0].balance
    }

    getUser()

    return {
      getUser,
      username,
      phone,
      password,
      firstname,
      lastname,
      balance
    }
  },
  components: {AppPage}
}
</script>

<style scoped>

</style>