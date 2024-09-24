import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home'
//import HelloWorld from '../components/HelloWorld'
import CreateComplaint from '../components/CreateComplaint'
import EvacuationRoute from '../components/EvacuationRoute'
import FloodableZone from '../components/FloodableZone'
import MeetingPoint from '../components/MeetingPoint'
import ShowComplaints from '../components/ShowComplaints'
import Statistics from '../components/Statistics'
import Zonainfo from '../components/Zonainfo.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/puntosDeEncuentros',
        name: 'Puntos de Encuentos',
        component: MeetingPoint
    },
    {
        path: '/recorridoDeEvacuacion',
        name: 'Recorridos de Evacuacion',
        component: EvacuationRoute
    },
    {
        path: '/zonasInundables',
        name: 'Zonas Inundables',
        component: FloodableZone
    },
    {
        path: '/crearDenuncia',
        name: 'Crear Denuncia',
        component: CreateComplaint
    },
    {
        path: '/verDenuncia',
        name: 'Ver Denuncia',
        component: ShowComplaints
    },
    {
        path: '/estadisticas',
        name: 'Estadisticas',
        component: Statistics
    },
    {
        path: '/verInfoZona/:id',
        name: 'verInfoZona',
        component: Zonainfo,
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router