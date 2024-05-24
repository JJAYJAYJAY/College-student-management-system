import {defineStore} from "pinia";
import {reactive, ref} from "vue";

const useUserStore=defineStore(
    'user',
    () => {
        const user = ref({
            role: '',
        })
        const setRole = (newRole) => {
           user.value.role = newRole;
        }
        return {
            user,
            setRole
        }
    }
)

export default useUserStore;