<template>
  <div class="modal-backdrop1" @click="$emit('close')"></div>
    <div id="myModal" class="modal1">
      <div class="modal-content1" style="text-align: center">
        <h3><strong>Этот стол уже забронирован!</strong> <br> <strong>Имя: {{firstname}} <br> Фамилия: {{lastname}} <br> Номер телефона: {{phone}}</strong></h3>
      </div>
    </div>
</template>

<script>
import {ref} from "vue"
export default {
  emits: ['close'],
  props: {
    firstname: String,
    lastname: String,
    username: String,
    phone: String
  }
}
</script>

<style scoped>
@media screen and (max-width: 700px) {
    .modal1 {
      position: fixed;
      top: 60px;
      width: 600px;
      padding: 1rem;
      background: #fff;
      z-index: 1000;
      left: 50%;
      border-radius: 10px;
      transform: translateX(-50%);
      box-shadow: 2px 3px 10px rgba(0, 0, 0, 0.2);
      max-width: 300px;
    }
  }
</style>