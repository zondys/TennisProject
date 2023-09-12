<template>
    <form class="card" @submit.prevent="onSubmit">
      <h1>Войти в систему</h1>

      <div :class="['form-control1', {invalid: eError}]">
        <label for="username">Логин</label>
        <input id="username" v-model="username" @blur="eBlur">
        <small v-if="eError">{{ eError }}</small>
      </div>

      <div :class="['form-control1', {invalid: pError}]">
        <label for="password">Пароль</label>
        <input type="password" id="password" v-model="password" @blur="pBlur">
        <small v-if="pError">{{ pError }}</small>
      </div>

      <router-link to="signUp" style="font-size: 20px; margin-bottom: 5px;">Зарегистрироваться!</router-link>
      <button class="btn primary item" type="submit" :disabled="isSubmitting">Войти</button>
    </form>
</template>

<script>
import {useLoginForm} from "@/use/login-form";
import {useRoute} from "vue-router/dist/vue-router";
import {useStore} from "vuex";
import {error} from "@/utils/error";

export default {
  setup() {
    const route = useRoute()
    const store = useStore()

    if (route.query.message) {
      store.dispatch('setMessage', {
        value: error(route.query.message),
        type: 'warning'
      })
    }
    return {...useLoginForm()}
  }
}
</script>

<style scoped>

</style>