import {defineStore} from "pinia";
import {reactive, ref} from "vue";

const useUserStore=defineStore(
    'user',
    () => {
        const user = ref({
            role: '',
            classId: '',
        })
        const setRole = (newRole) => {
           user.value.role = newRole;
        }

        const setClassId = (newClassId) => {
            user.value.classId = newClassId;
        }
        return {
            user,
            setRole,
            setClassId
        }
    }
)

export default useUserStore;