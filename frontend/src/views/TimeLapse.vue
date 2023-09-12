<template>
  <app-page title="Список столов">

    <form @submit.prevent="chooseDate" style="padding-bottom: 10px;">
      <div style="display:flex; margin: 0 -5px;" class='box'>
        <h2 class="item">Выберите дату:</h2>
      </div>

      <div style="display:flex; margin: 0 -5px;" class='box'>
        <input type="date" id="date" v-model="date" class='item'>
        <button class="btn primary item">Выбрать</button>
      </div>
    </form>


    <div>
      <table class="table bordered table-width" v-if="date !== null && timelapsestoday !== null">
        <thead>
        <tr>
          <th scope="col" style="width: 15%;">Время</th>
          <th scope="col" style="width: 17%;">Стол 1</th>
          <th scope="col" style="width: 17%;">Стол 2</th>
          <th scope="col" style="width: 17%;">Стол 3</th>
          <th scope="col" style="width: 17%;">Стол 4</th>
          <th scope="col" style="width: 17%;">Стол 5</th>
        </tr>
        </thead>

        <tbody style="height: 1000px;">
        <tr v-for="hour in 24" :key="hour">
          <td>{{ hour - 1 }}:00 - {{ hour }}:00</td>
          <td v-for="table in 5" :key="table" style="height: 40px;" @click="createTimeLapseTable(hour, table)">
            <div v-for="timelapse in timelapsestoday" :key="timelapse.id">
              <a v-if="(timelapse.time_lapse === hour) && (timelapse.table_number === table)">{{timelapse.username}}</a>
            </div>
          </td>
        </tr>
        </tbody>
      </table>

      <teleport to="body">
        <create-modal v-if="isOpenCreate" @close="isOpenCreate = false"></create-modal>
      </teleport>
      <teleport to="body">
        <delete-modal v-if="isOpenDelete" @close="isOpenDelete = false"></delete-modal>
      </teleport>
      <teleport to="body">
        <delete-confirm-modal v-if="isOpenDeleteConfirm" @close="isOpenDeleteConfirm = false"
                              :timelapsestoday="timelapsestoday" :i="DeleteI" :timelapses="timelapses"
                              :choose-date="chooseDate" :get-time-lapses="getTimeLapses" :balance="balance" :price="price" :id="id"></delete-confirm-modal>
      </teleport>
      <teleport to="body">
        <creation-confirm v-if="isOpenCreationConfirm" @close="isOpenCreationConfirm = false" :date="date"
                          :hour="timelapse.time_lapse" :table="timelapse.table_number"
                          @create-time-lapse="createTimeLapse" :price="price" :balance="balance"></creation-confirm>
      </teleport>
      <teleport to="body">
        <info-modal v-if="isOpenInfoModal" @close="isOpenInfoModal = false" :firstname="firstname" :lastname="lastname" :phone="phone"></info-modal>
      </teleport>
    </div>
  </app-page>
</template>

<script>
import AppPage from "@/components/ui/AppPage";
import AppLoader from "@/components/ui/AppLoader";
import axios from "axios";
import {ref} from "vue";
import {useStore} from "vuex";
import CreateModal from "@/components/ui/Modals/CreateModal";
import DeleteModal from "@/components/ui/Modals/DeleteModal";
import DeleteConfirmModal from "@/components/ui/Modals/DeleteConfirmModal";
import CreationConfirm from "@/components/ui/Modals/CreationConfirm";
import InfoModal from "@/components/ui/Modals/InfoModal";

export default {
  setup() {
    const timelapse = ref({username: '', date: '', table_number: 0, time_lapse: 0, id: 0})
    const timelapses = ref(null)
    const timelapsestoday = ref(null)
    const date = ref(null)
    const price = ref(200)

    const isOpenCreate = ref(false)
    const isOpenDelete = ref(false)
    const isOpenCreationConfirm = ref(false)
    const isOpenDeleteConfirm = ref(false)
    const DeleteConfirm = ref(null)
    const isOpenInfoModal = ref(false)

    const DeleteI = ref(null)
    const username = ref(null)
    const firstname = ref(null)
    const lastname = ref(null)
    const phone = ref(null)
    const balance = ref(null)
    const id = ref(null)

    const store = useStore()

    const getTimeLapses = async () => {
      const response = await axios.get('http://127.0.0.1:8000/api/timelapses/')
      timelapses.value = response.data
    }

    const getTimeLapsesDateFilter = async (date) => {
      const response = await axios.get('http://127.0.0.1:8000/api/timelapses/', {
        params: {
          date: date
        }
      })
      timelapsestoday.value = response.data
    }

    const chooseDate = async () => {
      await getTimeLapsesDateFilter(date.value)
    }

    const createTimeLapse = async () => {
      await getTimeLapses()

      await axios.post('http://127.0.0.1:8000/api/timelapses/', {
        date: timelapse.value.date,
        table_number: timelapse.value.table_number,
        time_lapse: timelapse.value.time_lapse,
        username: store.getters['auth/username']
      })

      console.log(balance.value - price.value)
      let newbalance = balance.value - price.value

      await axios.patch('http://127.0.0.1:8000/api/users/'+id.value+'/', {
        balance: newbalance
      })

      await getTimeLapses()
      await chooseDate()
    }

    const editTimeLapse = async () => {
      await getTimeLapses()

      await axios.put(`http://127.0.0.1:8000/api/timelapses/${timelapse.value.id}/`, timelapse.value)

      await getTimeLapses();
      timelapse.value = {username: '', date: '', table_number: '', time_lapse: '', id: ''};
    }

    const submitForm = () => {
      if (timelapse.value.id === undefined) {
        createTimeLapse();
      } else {
        editTimeLapse();
      }
    }

    const getUser = async (username) => {
      const {data} = await axios.get('http://127.0.0.1:8000/api/users/', {
        params: {
          username: username
        }
      })

      firstname.value = data[0].first_name
      lastname.value = data[0].last_name
      phone.value = data[0].phone
      balance.value = data[0].balance
      id.value = data[0].id
    }

    const checkDate = (hour_table, real_hour) => {
      const CurrentTime = new Date().toLocaleTimeString('ru-RU', {timeZone: 'Europe/Moscow'})
      const CurrentDate = new Date().toLocaleDateString('ru-RU', {timeZone: 'Europe/Moscow'})

      let parts = date.value.split('-')
      let parts1 = CurrentDate.split('.')
      let parts2 = CurrentTime.split(':')

      const DateTimelapse = new Date(parts[0], parts[1] - 1, parts[2])
      const DateTimeNow = new Date(parts1[2], parts1[1] - 1, parts1[0], parts2[0], parts2[1], parts2[2])

      return DateTimelapse.getFullYear() < DateTimeNow.getFullYear() || DateTimelapse.getFullYear() === DateTimeNow.getFullYear()
          && DateTimelapse.getMonth() < DateTimeNow.getMonth() ||
          DateTimelapse.getFullYear() === DateTimeNow.getFullYear() && DateTimelapse.getMonth() === DateTimeNow.getMonth()
          && DateTimelapse.getDate() < DateTimeNow.getDate() ||
          DateTimelapse.getFullYear() === DateTimeNow.getFullYear() && DateTimelapse.getMonth() === DateTimeNow.getMonth()
          && DateTimelapse.getDate() === DateTimeNow.getDate() && hour_table < DateTimeNow.getHours() + real_hour
    }

    const createTimeLapseTable = async (hour, table) => {
      if (timelapsestoday.value.length === 0) {
          timelapse.value.date = date.value
          timelapse.value.time_lapse = hour
          timelapse.value.table_number = table
          timelapse.value.username = ''
      }

      for (let i = 0; i < timelapsestoday.value.length; i++) {
        if (timelapsestoday.value[i].date === date.value && timelapsestoday.value[i].time_lapse === hour &&
            timelapsestoday.value[i].table_number === table) {
          timelapse.value.date = date.value
          timelapse.value.time_lapse = hour
          timelapse.value.table_number = table
          timelapse.value.id = i
          timelapse.value.username = timelapsestoday.value[i].username
          break
        } else {
          timelapse.value.date = date.value
          timelapse.value.time_lapse = hour
          timelapse.value.table_number = table
          timelapse.value.username = ''
        }
      }


      if (timelapse.value.username === store.getters['auth/username']) {
        if (checkDate(hour, 3)) {
          isOpenDelete.value = true
          return
        } else {
          username.value = timelapse.value.username
          await getUser(username.value)
          DeleteI.value = timelapse.value.id
          isOpenDeleteConfirm.value = true
          return
        }
      } else if (timelapse.value.username !== '') {
        username.value = timelapse.value.username
        await getUser(username.value)
        isOpenInfoModal.value = true
        return
      } else {
        if (checkDate(hour, 2)) {
          isOpenCreate.value = true
          return
        } else {
          username.value = store.getters['auth/username']
          await getUser(username.value)
          console.log(balance.value)
          timelapse.value.username = store.getters['auth/username']
          isOpenCreationConfirm.value = true
        }
      }
    }


    return {
      getTimeLapses,
      submitForm,
      editTimeLapse,
      createTimeLapse,
      chooseDate,
      getTimeLapsesDateFilter,
      createTimeLapseTable,
      timelapse,
      timelapses,
      timelapsestoday,
      date,
      isOpenCreate,
      isOpenDelete,
      isOpenDeleteConfirm,
      DeleteConfirm,
      DeleteI,
      isOpenCreationConfirm,
      isOpenInfoModal,
      username,
      firstname,
      lastname,
      phone,
      price,
      balance,
      id
    }
  },
  components: {
    CreateModal,
    AppLoader,
    AppPage,
    DeleteModal,
    DeleteConfirmModal,
    CreationConfirm,
    InfoModal
  }
}
</script>

<style scoped>
.box {
  display: flex;
}

.item {
  margin: 0 5px;
}

.table-width {
  max-width: 1475px;
}

@media screen and (max-width: 500px) {
  .table-width {
    overflow-x: auto;
  }
}
</style>