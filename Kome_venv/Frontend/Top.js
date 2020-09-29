//1.ルートコンポーネントを定義
const Registration_Field = {template: `<regist-field></regist-field>`}
const Reservation_Field = { template: `<reserve-field></reserve-field>` }


//2.ルートを定義
// 各ルートは 1 つのコンポーネントとマッピングされる必要があります。
// このコンポーネントは実際の `Vue.extend()`、
// またはコンポーネントオプションのオブジェクトでも構いません。
// ネストされたルートに関しては後で説明します
const routes =[
    {path: '/Registration_Field', component: Registration_Field},
    {path: '/Reservation_Field', component: Reservation_Field}


]

// 3. ルーターインスタンスを作成して、ルートオプションを渡します
// 追加のオプションをここで指定できますが、
// この例ではシンプルにしましょう
const router = new VueRouter({
    routes // `routes: routes` の短縮表記
  })

// 4. root となるインスタンスを作成してマウントします
// アプリケーション全体がルーターを認知できるように、
// ルーターをインジェクトすることを忘れないでください。
const app = new Vue({
  el: '#app',
  router
  })
  //.$mount('#app')





