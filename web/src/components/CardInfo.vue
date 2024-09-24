<template>
  <div class="col-12 col-md-4  py-2">
        <div class="card w-100 mt-3 border-secondary border-radius-50" style="width: 18rem;">
          <img :src="require('../assets/img/cardinfo/'+img)" class="card-img-top" alt="">
          <div class="card-body "> 
            <h4 class="card-title text-center ">{{title}}</h4>
            <p class="card-text text-center">{{description}}</p>
             <router-link v-bind:to="'/'+link" class="btn btn-info btn-lg btn-block">Ingresar </router-link>
          </div>
        </div>
      </div>
</template>
<script>
export default {
  name: 'CardInfo',
  props: {
    title: String,
    description: String,
    link: String,
    img: String
  },
  data: () => ({
        
    }),
}
</script>