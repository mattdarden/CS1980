drop table if exists classes_taken cascade;
drop table if exists courses_info cascade;
drop table if exists demographics cascade;
drop table if exists finance cascade;
drop table if exists hs_tests cascade;
drop table if exists major cascade;
drop table if exists academics cascade;

create table classes_taken (
    analytics_id int not null,
    academic_term_code int,
    term_desc varchar(30),
    cat_num int,
    sub_code int,
    sub_desc varchar(5),
    class_num int,
    class_sec_num int,
    title varchar(10),
    grade varchar(2),
    grading_basis int,
    grading_desc varchar(20),
    constraint classes_taken_pk primary key (analytics_id)
);

create table courses_info (
    term_code int not null,
    term_desc varchar(30),
    cat_num int,
    sub_code int,
    sub_desc varchar(30),
    class_num int,
    class_sec_num int,
    title varchar(30),
    inst_name varchar (30),
    inst_role_desc varchar(30),
    facility varchar (20),
    building_code char(5),
    room char(5),
    room_cap int,
    enroll_cap int,
    wait_cap int,
    start_date date,
    end_date date,
    start_time time,
    end_time time,
    constraint courses_info_pk primary key (term_code)
);

create table demographics (
    analytics_id int not null,
    max_age int,
    ethnic_group_code char(5),
    ethnic_group_desc varchar(30),
    gender varchar(10),
    citizen_status varchar(10),
    first_gen_desc varchar(10),
    in_out_state char(2),
    home_state varchar(15),
    citizen_country int,
    constraint demo_pk primary key (analytics_id)
);

create table finance(
    analytics_id int,
    aid_year int,
    aid_year_desc varchar(30),
    fafsa_flag char(1),
    income_lvl_desc varchar(30),
    house_desc varchar(30),
    constraint finance_pk primary key (analytics_id)
);

create table hs_tests(
    analytics_id int,
    hs_gpa real,
    test_name varchar(10),
    test_comp varchar(25),
    test_date date,
    constraint hs_tests_pk primary key (analytics_id)
);

create table major (
    analytics_id int,
    app_num int,
    admit_term_code int,
    admit_term_desc varchar(25),
    acdm_plan_desc varchar(25),
    acdm_plan_type varchar(10),
    acdm_sub_plan_type varchar(10),
    acdm_group_code varchar(40),
    acdm_prgm_code int,
    acdm_prgm_desc varchar(25),
    app_cnt_code int,
    app_cnt_desc varchar(25),
    admit_type_code int,
    admit_type_desc varchar(25),
    prgm_action_code int,
    prgm_action_desc varchar(25),
    house_intst_desc varchar(25),
    res_code int,
    res_desc varchar (25),
    constraint major_pk primary key (analytics_id)
);

create table academics (
    analytics_id int,
    acdm_term_code int,
    acdm_term_desc varchar(25),
    pell_elg_flag int,
    curr_gpa real,
    acdm_std_act_code int,
    acdm_std_act_desc varchar(25),
    degree_chkt_status_code int,
    degree_chkt_status_desc varchar(25),
    acdm_career_code int,
    constraint academics_pk primary key (analytics_id)
);