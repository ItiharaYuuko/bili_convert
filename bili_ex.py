import os, shutil, json, re, sys
import pprint as pp

def convert_process(in_v, in_a, out_v):
    commd = 'ffmpeg -i \'%s\' -i \'%s\' -codec copy \'%s\'' % (in_v, in_a, out_v)
    os.system(commd)

def gen_json_data(ent_f_name):
    with open(ent_f_name, 'r+') as f_json:
        t_da = json.load(f_json)
        tpx = {}
        if t_da.get('ep') == None:
            tpx = {t_da.get('page_data').get('page'): t_da.get('page_data').get('part')}
        else:
            tpx = {t_da.get('ep').get('episode_id'): t_da.get('title') + t_da.get('ep').get('index')}
        return tpx

def rt_dir():
    p_list = [i for i in os.listdir() if os.path.isdir(i)]
    return p_list

def itor_process(aim_pa):
    name_match = re.compile(r'\D+')
    f_o_m_str = r'^\.+'
    f_o_match = re.compile(f_o_m_str)
    th_base_pa = os.getcwd()[:-2]
    json_f_name = 'entry.json'
    os.chdir(aim_pa)
    name_dic_list = []
    
    for rn_dir in rt_dir():
        v_info = gen_json_data(rn_dir + '/' + json_f_name)
        n_p_name = str([k for k in v_info.keys()][0])
        
        if str(rn_dir) != n_p_name:
            t_n_dic = {str(rn_dir): n_p_name}
            name_dic_list.append(t_n_dic)
    
    if len(name_dic_list) > 0:
        for it_dic in name_dic_list:
            for (k, v) in it_dic.items():
                os.rename(k, v)
    
    for p_dir in rt_dir():
        os.chdir(p_dir)
        v_info = gen_json_data(json_f_name)
        lv_n = ''

        try:
            lv_n = v_info.get(int(p_dir))
        except ValueError as verr:
            print('The forlder not named for integer   %s' % verr)
            lv_n = v_info.get(p_dir)

        if f_o_match.match(lv_n):
            lv_n = re.sub(f_o_m_str, '', lv_n)

        tf_n = rt_dir()[0]
        b_pa = os.getcwd() + ('/%s/' % tf_n)
        in_v_n = b_pa + 'video.m4s'
        in_a_n = b_pa + 'audio.m4s'
        st_fd = ''

        try:
            st_fd = th_base_pa + '/' + name_match.findall(lv_n)[0]
        except TypeError as terr:
            print('Match type error %s' % terr)
            st_fd = th_base_pa + '/' + lv_n
        #st_fd = th_base_pa + '/' + lv_n
        out_v_n = st_fd + '/' + lv_n + '.mp4'
        
        if os.path.exists(st_fd):
            convert_process(in_v_n, in_a_n, out_v_n)
        else:
            os.mkdir(st_fd)
            convert_process(in_v_n, in_a_n, out_v_n)
            
        if os.getcwd().split('/')[-1] == p_dir:
            os.chdir('..')

if __name__ == '__main__':
    for i in rt_dir():
        itor_process(i)
        os.chdir('..')