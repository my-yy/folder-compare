import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: HomeView
    },
    {
        path: '/collection/:id?',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/CollectionView.vue')
    },
    {
        path: '/raw/:id?',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/CollectionViewRaw.vue')
    },
    {
        path: '/edit',
        component: () => import(/* webpackChunkName: "about" */ '../tests/TestEditor.vue')
    },
    {
        path: '/grid',
        component: () => import(/* webpackChunkName: "about" */ '../tests/TestGrid.vue')
    },
    {
        path: '/table',
        component: () => import(/* webpackChunkName: "about" */ '../tests/TestTable.vue')
    },
    {
        path: '/figure/:id?',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/FigureView.vue')
    },
]

const router = new VueRouter({
    routes
})

export default router
