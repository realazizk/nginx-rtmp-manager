import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = {
  en: {
    name: 'Radio',
    login: 'Login',
    contact: 'Contact',
    home: 'Home',

    loginp: {
      message: 'Please sign in',
      username: 'Username',
      password: 'Password',
      remember: 'Remember me',
      button: 'Sign in'
    },

    stream: {
      audio: 'audio',
      live: 'live',
      video: 'video',
      list: 'List of streams'
    },

    menu: {
      actions: 'User actions',
      stream: 'Stream',
      addstream: 'Add stream',
      managestreams: 'Manage streams',
      jobs: 'Jobs',
      managejobs: 'Manage jobs',
      addjob: 'Add job',
    },

    bar: {
      logout: "Logout"
    },

    addstreammodal: {
      title: 'Add stream',
      url: 'The stream url',
      password: 'Password',
      stype: 'Select stream type',
      submit: 'Submit'
    },

    streamsp: {
      delete: 'Delete',
      streamtype: 'Stream Type',
      streamname: 'Stream Name',
      remove: 'Remove',
      edit: 'Edit',
    },

    jobsp: {
      streamchannel: 'Stream Channel',
      starttime: 'Start time UTC',
      endtime: 'End time UTC',
      filename: 'File name'
    },

    lang: {
      l: 'Language',
      ls: [{
	name: 'Arabic',
	code: 'ar'}, {name: 'English', code: 'en'}]
    }
    ,

    
    
    editstreammodal: {
      title: 'Edit stream'
    },

    addjobmodal: {
      title: 'add job',
      inf: 'Infinite playback',
      playnow: 'Play now',
      shuffle: 'Shuffle playlist',
      enterdate: 'Enter date',
      channel: 'Select the channel to stream to stream to',
      submit: 'submit'
    }


  },
  ar: {
    name: 'راديو',
    login: 'دخول',
    contact: 'توصل معنا',
    home: 'الرئيسية',
    
    loginp: {
      message: 'الرجاء تسجيل الدخول',
      username: 'اسم المستخدم',
      password: 'كلمه السر',
      remember: 'تذكرنى',
      button: 'تسجيل الدخول',
      
    },

    stream: {
      audio: 'صوت',
      live: 'مباشر',
      video: 'فيديو',
      list: 'قائمة الجداول'
    },
    menu: {
      actions: 'إجراءات المستخدم',
      stream: 'ستريم',
      addstream: 'إضافة ستريم',
      managestreams: 'إدارة مجموعات البث',
      jobs: 'وظائف',
      managejobs: 'إدارة الوظائف',
      addjob: 'إضافة وظيفة',
    },

    bar: {
      logout: "الخروج"
    },

    addstreammodal: {
      title: 'إضافةstream',
      url: 'عنوان ورل للتيار',
      password: 'كلمه السر',
      stype: 'حدد نوع البث',
      submit: 'إرسال'
    },

    streamsp: {
      delete: 'حذف',
      streamtype: 'نوع البث',
      streamname: 'اسم تيار',
      remove: 'إزالة',
      edit: 'تصحيح'
    },

    jobsp: {
      streamchannel: 'قناة البث',
      starttime: 'وقت البدء UTC',
      endtime: 'وقت النهاية UTC',
      filename: 'اسم الملف'
    },

    lang: {
      l: 'لغة',
      ls: [{
	name: 'عربى',
	code: 'ar'
      },
	   {
	     name: 'الإنجليزية',
	     code: 'en'
	   }
	  ]
    },

    editstreammodal: {
      title: 'تحرير تيار',
      
    },

    addjobmodal: {
      title: 'إضافة وظيفة',
      inf: 'تشغيل لانهائية',
      playnow: 'العب الآن',
      shuffle: 'قائمة التشغيل المراوغة',
      enterdate: 'أدخل التاريخ',
      channel: 'قم بتحديد القناة إلى تيار إلى تيار إلى',
      submit: 'إرسال'
    }
    
  }
}


export default new VueI18n({
  locale: 'ar',
  messages
})
