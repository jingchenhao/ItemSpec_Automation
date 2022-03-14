#!/usr/bin/env python
# coding: utf-8

# In[1056]:


import jinja2
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None 


# In[1057]:


data_dir=('/Users/jing.chen/OneDrive - Northwest Evaluation Association/Documents/NWEA/'+                        'NCME_2022/ItemSpec/')
output_dir=('/Users/jing.chen/OneDrive - Northwest Evaluation Association/Documents/NWEA/'+                        'NCME_2022/ItemSpec/archive/')


# In[1058]:


def recode_col(df,col):
    for i in range (df.shape[0]):
        content = df[col][i].replace('\n\n','\n')
        lines = content.split('\n')
        for j in range(len(lines)):
            lines[j] ='• ' + lines[j]
            text = '\n'.join(lines)
            text = text.replace('\n','\\newline')
            df[col][i] = text
    return (df)


# In[1059]:


def recode_to_verb(df,col):
    df[col+'_verb']= np.nan
    for i in range (df.shape[0]):
        lines = df[col][i].split('\n\n')
        verb_list=[]
        for j in range(len(lines)):
            verb = lines[j].split(' ')[0]
            if verb not in verb_list:
                verb_list.append(verb)
        df[col+'_verb'][i] = verb_list
    return (df)


# In[1060]:


def verb_to_itemtype(df,col):
    df[col+'_itemtype']= np.nan
    for i in range (df.shape[0]):
        v = df[col][i]
        types_list=[]
        for j in range(len(v)):
            types = verb_itemtype_dic.get(v[j])
            for k in range(len(types)):
                if types[k] not in types_list:
                    types_list.append(types[k])
                else:
                    continue
            #print(i,j,v,v[j],types,types_list)
        df[col+'_itemtype'][i] = sorted(types_list)
    return (df)


# In[1061]:


def recode_itemtype(df,col):
    for i in range (df.shape[0]):
        content = df[col][i]
        for j in range(len(content)):
            content[j] = '• '+content[j]#'• '
            text = '\\newline'.join(content)        
        df[col][i] = text
    return (df)


# In[1062]:


DF = pd.read_excel(data_dir+'g6_sample_for_NCME.xlsx',sheet_name='ALL')


# In[1063]:


verb_table = pd.read_excel(data_dir+'g6_sample_for_NCME.xlsx',sheet_name='verb')


# In[1064]:


verb_itemtype=[]
for i in range(verb_table.shape[0]):
    verb = verb_table.Verbs[i]
    itemtype = []
    for j in range(verb_table.shape[1]):
        if verb_table.iloc[i,j]=='x':
            itemtype.append(verb_table.columns[j])
        else:
            continue
    verb_itemtype.append((verb,itemtype))


# In[1065]:


verb_itemtype = pd.DataFrame(verb_itemtype).rename(columns={0:'Verbs',1:'itemtypes'})
verb_itemtype_dic = dict(zip(verb_itemtype.Verbs,verb_itemtype['itemtypes']))


# In[1066]:


verb_table = pd.merge(verb_table[['Verbs','Definition']],verb_itemtype,on = 'Verbs',how='inner')


# In[1067]:


DF = recode_to_verb(DF,'ALD1')
DF = recode_to_verb(DF,'ALD2')
DF = recode_to_verb(DF,'ALD3')


# In[1068]:


DF = verb_to_itemtype(DF,'ALD1_verb')
DF = verb_to_itemtype(DF,'ALD2_verb')
DF = verb_to_itemtype(DF,'ALD3_verb')


# In[1070]:


DF = recode_col(DF,'ALD1')
DF = recode_col(DF,'ALD2')
DF = recode_col(DF,'ALD3')


# In[1071]:


DF = recode_itemtype(DF,'ALD1_verb_itemtype')
DF = recode_itemtype(DF,'ALD2_verb_itemtype')
DF = recode_itemtype(DF,'ALD3_verb_itemtype')


# In[1072]:


verb_table_recoded = recode_itemtype(verb_table,'itemtypes')


# In[1073]:


latex_jinja_env= jinja2.Environment(
       block_start_string='\BLOCK{',
       block_end_string='}',
       variable_start_string='\VAR{',
        variable_end_string='}',
       comment_start_string='\#{',
       comment_end_string='}',
       line_statement_prefix='%%',
       line_comment_prefix='%#',
       trim_blocks=True,
       autoescape=False,
       loader = jinja2.FileSystemLoader('/Users/jing.chen/OneDrive - Northwest Evaluation Association/Documents/'+\
                                         'NWEA/NCME_2022/ItemSpec/'))


# In[1074]:


template = latex_jinja_env.get_template('item_spec_template.tex')


# In[1075]:


rendered_tex_list=[]
for i in range (DF.shape[0]):
    rendered_tex = template.render(ver_tab = verb_table_recoded,                                   stan = DF.subgoal[i],indi = DF.IND[i],                                   ald1 = DF.ALD1[i],ald2 = DF.ALD2[i],ald3 = DF.ALD3[i],                                  mdok1 = DF.ALD1_mdok[i],mdok2 = DF.ALD2_mdok[i],mdok3 = DF.ALD3_mdok[i],                                  itemtype1 = DF.ALD1_verb_itemtype[i],itemtype2 = DF.ALD2_verb_itemtype[i],itemtype3 = DF.ALD3_verb_itemtype[i])
    rendered_tex_list.append(rendered_tex)


# In[1076]:


for i in range(DF.shape[0]):
    with open(output_dir+'item_spec_updated'+str(i)+'.tex', 'w') as output:
            output.write(rendered_tex_list[i])


# In[1077]:


verb_template = latex_jinja_env.get_template('verb_table_template.tex')
verb_rendered_tex = verb_template.render(ver_tab = verb_table_recoded)
with open(output_dir+'verb_table_updated.tex', 'w') as output:
            output.write(verb_rendered_tex)


# In[ ]:




