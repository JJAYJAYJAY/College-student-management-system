export const MENU = {
    student: {
        '信息查询':{
            icon:'icon-apps',
            menuItem:[
                {
                    name:"成绩查询",
                    path:"score"
                },
                {
                    name:"课表查询",
                    path:"schedule"
                },
                {
                    name:"开课信息查询",
                    path:"courseOffering"
                }
            ]
        },
        '个人信息':{
            icon:'icon-user',
            menuItem:[
                {
                    name:"个人信息",
                    path:"studentProfile"
                }
            ]
        }
    },
    teacher:{
        '信息查询':{
            icon:'icon-apps',
            menuItem:[
                {
                    name:"任课信息查询",
                    path:"courseInfo"
                }
            ]
        },
        '个人信息':{
            icon:'icon-user',
            menuItem:[
                {
                    name:"个人信息",
                    path:"teacherProfile"
                }
            ]
        },
        '教学管理':{
            icon:'icon-archive',
            menuItem:[
                {
                    name:"成绩录入",
                    path:"scoreInput"
                }
            ]
        }
    },
    admin:{
        "信息查询":{
            icon:'icon-apps',
            menuItem:[
                {
                    name:"学生信息",
                    path:"studentInfo"
                },
                {
                    name:"教师信息",
                    path:"teacherInfo"
                }
            ]
        },
        "课程管理":{
            icon:'icon-archive',
            menuItem:[
                {
                    name:"学生信息录入",
                    path:"studentInfoInput"
                },
                {
                    name:"教师信息录入",
                    path:"teacherInfoInput"
                },
                {
                    name:"开课录入",
                    path:"courseOfferingInput"
                }
            ]
        },
    }
}