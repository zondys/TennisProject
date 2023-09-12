<template>
  <div class="modal-backdrop1" @click="$emit('close')"></div>
    <div id="myModal" class="modal1">
      <div class="modal-content1" style="text-align: center">
        <h3><strong>Ваш баланс: {{balance}} руб.</strong></h3>
        <h3><strong>Вы уверены, что хотите записаться на {{date}} c {{hour - 1}}:00 до {{hour}}:00 на стол номер {{table}} за {{price}} руб?</strong></h3>
        <button class="btn primary" v-if="balance >= price" @click="$emit('CreateTimeLapse'); $emit('close')">Да</button>
        <button class="btn primary disabled" v-else>Да</button>
        <button class="btn warning" @click="$emit('close')">Нет</button>
      </div>
    </div>
</template>

<script>
import {ref} from "vue";
export default {
  emits: ['close', 'CreateTimeLapse'],
  props: {
     date: {
      type: String
    },
     hour: {
      type: Number
    },
    table: {
      type: Number
    },
    balance: {
       type: Number
    },
    price: {
       type: Number
    }
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