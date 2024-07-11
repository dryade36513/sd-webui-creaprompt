import contextlib
import os
import gradio as gr
import random
import pandas as pd
from gradio import components as grc
from modules import scripts
from modules import script_callbacks

script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "../csv/" )
notactive = "未啟動"
active = "啟動"
dropdowns = []

def send_text_to_prompt(new_text, old_text, Prefix, sufix):
    if Prefix:
        new_text = Prefix + "," + new_text
    if sufix:
        new_text = new_text + "," + sufix
    return new_text
    
def send_before_prompt(new_text, old_text):
    return new_text + "," + old_text
    
def send_after_prompt(new_text, old_text):
    return old_text + "," + new_text    
    
def read_random_line_from_csv_files(checkbox_group):
    chosen_lines = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename[3:-4] in checkbox_group:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    chosen_lines.append(random.choice(lines).strip())
    concatenated_lines = ",".join(chosen_lines) if chosen_lines else "請選擇一個類別。"
    return concatenated_lines
    
def read_random_line_from_csv_files_auto(checkbox_group_manu):
    chosen_lines = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename[3:-4] in checkbox_group_manu:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    chosen_lines.append(random.choice(lines).strip())
    concatenated_lines = ",".join(chosen_lines) if chosen_lines else "請選擇一個類別。"
    return concatenated_lines
   
def select_random_line_from_collection():
    file_path = os.path.join(folder_path, "collection.txt")
    if os.path.exists(file_path) and file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            readline = random.choice(lines).strip()
            if lines:
                return readline
            else:
                return "檔案是空的。"
    else:
        return "指定的檔案不存在或不是文字檔案。"  

def read_random_line_from_csv_file_manual(dropdown_index):
    chosen_lines = []
    i = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and i == dropdown_index:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    chosen_lines.append(random.choice(lines).strip())
        i += 1
    concatenated_lines = "".join(chosen_lines)
    return concatenated_lines
        
def getfilename():
    name = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
           name.append(filename[3:-4])
    return name
    
def get_config_files():
    config_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".config"):
            config_files.append(filename[:-7])
    return config_files
    
def load_checkbox_state(selected_file):
    if not selected_file:
        print("請選擇一個檔案。")
        return
    file_path = os.path.join(folder_path, selected_file + ".config")
    with open(file_path, "r") as file:
        lines = file.readlines()
        selected_checkboxes = [line.strip() for line in lines]
    return selected_checkboxes
    
def save_checkbox_state(checkbox_group, file_name):
                if not file_name:
                  print("請輸入檔案名稱。")
                  return gr.update(choices=get_config_files()), gr.update(choices=get_config_files())
                if not file_name.endswith('.config'):
                  file_name += '.config'
                  file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as file:
                  for checkbox in checkbox_group:
                    file.write(f"{checkbox}\n")
                print("複選框狀態已成功儲存。")
                return gr.update(choices=get_config_files(), value= file_name[:-7]), gr.update(choices=get_config_files()) 
                
def save_checkbox_state_manu(checkbox_group_manu, file_name):
                if not file_name:
                  print("請輸入檔案名稱。")
                  return gr.update(choices=get_config_files()), gr.update(choices=get_config_files())
                if not file_name.endswith('.config'):
                  file_name += '.config'
                  file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as file:
                  for checkbox in checkbox_group_manu:
                    file.write(f"{checkbox}\n")
                print("複選框狀態已成功儲存。")
                return gr.update(choices=get_config_files(), value= file_name[:-7]), gr.update(choices=get_config_files())

def uncheck_auto_box(is_collection_enabled, is_enabled, is_manual_enabled):
    if not is_collection_enabled and not is_enabled and not is_manual_enabled:
      return None, None
    return not is_collection_enabled, not is_collection_enabled
    
def uncheck_auto_collection(is_enabled, is_collection_enabled, is_manual_enabled):
    if not is_collection_enabled and not is_enabled and not is_manual_enabled:
       return None, None
    return not is_enabled, not is_enabled
    
def uncheck_auto_manual(is_manual_enabled, is_collection_enabled, is_enabled ):
    if not is_collection_enabled and not is_enabled and not is_manual_enabled:
      return None, None
    return not is_manual_enabled, not is_manual_enabled

    
def handle_dropdown_change(selected_value, dropdown_index):
    concatenated_values = ""
    if selected_value == "🎲隨機\n":
       i = 0
       for filename in os.listdir(folder_path):
         if filename.endswith(".csv") and i == dropdown_index:
            selected_value = "🎲隨機: " + filename[3:-4] + "🎲"
            dropdown_values[dropdown_index] = selected_value
         i += 1
    else:
        if selected_value == "無\n":
           selected_value =""
           dropdown_values[dropdown_index] = selected_value[1:]
        else:
           dropdown_values[dropdown_index] = selected_value[1:]
    for value in dropdown_values:
        if value:
            concatenated_values += value + ","
    concatenated_values = concatenated_values.rstrip(", ")
    return concatenated_values
    
def none_dropdown_change(selected_value, dropdown_index):
        return gr.update(value= "無\n")
        
def none_dropdown_change_clear():
        selected_value =""
        for i, value in enumerate(dropdown_values):
            dropdown_values[i] = selected_value[1:]
        return selected_value
        
checkboxes = getfilename()          

class CreaPromptScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()
        
    def title(self):
        return "CreaPrompt"

    def show(self, is_img2img):
        return scripts.AlwaysVisible
        
    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("🎨CreaPrompt : 未啟動",open = False) as acc:
              gr.Markdown("""
                            <center><font size="4">
                                🧠CreaPrompt，瘋狂提示者的工具箱🧠
                                </font>
                                <br>
                                為了獲得最佳效果，請使用 <a href="https://civitai.com/models/383364?modelVersionId=539661">CreaPrompt_Ultimate </a> 檢查點
                            </center><br>
                            """)
              with gr.Accordion("➡️CreaPrompt 集合", open=False):
                     gr.Markdown("啟用時，只需按下正常的生成按鈕，也適用於批量處理")
                     with gr.Row():
                       is_collection_enabled = grc.Checkbox(label="♻️啟用自動提示", info="💬來自 CreaPrompt 集合", value=False)
                       is_randomize_manu = grc.Checkbox(label="🎲啟用隨機提示", info="💬對於批次中的每個圖片", value=False, interactive=True)
              with gr.Accordion("➡️從類別自動提示", open=True):
                with gr.Tab("✨隨機"):
                     with gr.Column(scale=3):
                       gr.Markdown("啟用時，選擇類別並按下正常的生成按鈕，也適用於批量處理")
                     with gr.Row():
                       is_enabled = grc.Checkbox(label="♻️啟用自動提示", info="💬從選定的類別", value=False)
                       is_randomize = grc.Checkbox(label="🎲啟用隨機提示", info="💬對於批次中的每個圖片", value=False, interactive=True)  
                     with gr.Row():
                       gr.Markdown("# ")
                     with gr.Column(scale=3):
                       prefix_auto = grc.Textbox(label="提示的前綴：", elem_id="auto_prompt_prefix", show_label=True, lines=2, placeholder="輸入你的前綴或留空如果你不需要", container=True)
                       sufix_auto = grc.Textbox(label="提示的後綴：", elem_id="auto_prompt_sufix", show_label=True, lines=2, placeholder="輸入你的後綴或留空如果你不需要", container=True)
                     with gr.Row():        
                       gr.Markdown("# ")
                     with gr.Column():
                       gr.Markdown("#")
                       checkbox_group = grc.CheckboxGroup(label="選擇類別：", choices=checkboxes, default=['base'], min_width=50)
                     with gr.Row():
                       gr.Markdown("#")    
                     with gr.Row():                      
                       save_state_button = gr.Button("儲存你的預設類別", elem_id="save_state", variant="primary")
                       file_name_textbox = grc.Textbox(elem_id="file_name", show_label=False, placeholder="輸入你的預設名稱", container=True)
                       file_dropdown_component = gr.Dropdown(show_label=False, choices=get_config_files(), elem_id="file_dropdown", value="選擇一個預設")
                with gr.Tab("✨手動"):
                    with gr.Row():
                      gr.Markdown("啟用時，從選單中選擇你想要的選項，然後按下正常的生成按鈕，也適用於批量處理")
                    with gr.Row():
                      is_manual_enabled = grc.Checkbox(label="♻️啟用自動提示", info="💬從下拉選單中選擇", value=False)
                      is_manual_random = grc.Checkbox(label="🎲啟用隨機提示", info="💬對於批次中的每個圖片", value=False, interactive=True)
                    with gr.Row():
                      gr.Markdown("# ")
                    with gr.Column(scale=3):
                      prefix_manual = grc.Textbox(label="提示的前綴：", elem_id="manual_prompt_prefix", show_label=True, lines=2, placeholder="輸入你的前綴或留空如果你不需要", container=True)
                      sufix_manual = grc.Textbox(label="提示的後綴：", elem_id="manual_prompt_sufix", show_label=True, lines=2, placeholder="輸入你的後綴或留空如果你不需要", container=True)
                      auto_final = grc.Textbox(label="提示預覽：", elem_id="manual_prompt_result", show_label=True, lines=2, placeholder="將使用的提示", interactive=False, container=True)
                      gr.Markdown("# ")
                      all_none_button = gr.Button("將所有類別設為無並清空提示列表，這可能需要幾秒鐘", elem_id="all_none", variant="primary")
                    with gr.Row():
                      gr.Markdown("# ")
                    with gr.Row():
                      gr.Markdown("# ")  
                    with gr.Row():
                      for filename in os.listdir(folder_path):
                        if filename.endswith(".csv"):
                           file_path = os.path.join(folder_path, filename)
                           lines = []
                           with open(file_path, 'r', encoding='utf-8') as file:
                              lines = file.readlines()
                           lines = ["➡️" + line.strip() for line in lines]
                           lines.insert(0, "無\n")
                           lines.insert(1, "🎲隨機\n")
                           dropdown_component = grc.Dropdown(label=f"{filename[3:-4]}", choices=lines, elem_id=f"{filename}_dropdown", container=True, value="無")
                           dropdowns.append(dropdown_component)
                    global dropdown_values
                    dropdown_values = [""] * len(dropdowns) 
              with gr.Accordion("➡️從類別手動創建提示", open=False):         
                     with gr.Column(scale=3):
                       gr.Markdown("💬按下正常的生成按鈕以使用最終提示生成圖像")
                       final = grc.Textbox(label="將用於生成圖像的最終提示：", elem_id="creaprompt_prompt_final", show_label=True, lines=2, placeholder="最終提示顯示在這裡", container=True)
                       Prefix = grc.Textbox(label="提示的前綴：", elem_id="prompt_prefix", show_label=True, lines=2, placeholder="輸入你的前綴或留空如果你不需要", container=True)
                       sufix = grc.Textbox(label="提示的後綴：", elem_id="prompt_sufix", show_label=True, lines=2, placeholder="輸入你的後綴或留空如果你不需要", container=True)
                       prompt = grc.Textbox(label="從類別創建的提示：", elem_id="promptgen_prompt", show_label=True, lines=2, placeholder="選擇你的選項並按下生成按鈕", container=True)
                       gr.Markdown("# ")
                       checkbox_group_manu = grc.CheckboxGroup(label="選擇類別：", choices=checkboxes, default=['base'], min_width=50)
                       gr.Markdown("# ")
                       with gr.Row():
                            save_state_button_manu = gr.Button("儲存你的預設類別", elem_id="save_state_manu", variant="primary")
                            file_name_textbox_manu = grc.Textbox(elem_id="file_name_manu", show_label=False, placeholder="輸入你的預設名稱", container=True)
                            file_dropdown_component_manu = gr.Dropdown(show_label=False, choices=get_config_files(), elem_id="file_dropdown_manu", value="選擇一個預設")
                       with gr.Row():
                            gr.Markdown("# ")
                       with gr.Row():
                            Sendbefore = gr.Button('在最終提示前添加', elem_id="promptgen_sendto_img", variant='primary')
                            send_text_button = gr.Button(value='替換最終提示', variant='primary')
                            Sendafter = gr.Button('在最終提示後添加', elem_id="promptgen_sendto_txt", variant='primary')                            
                       with gr.Column(scale=1):
                            gr.Markdown("#")
                            with gr.Row():
                                submit = gr.Button('從類別創建提示', elem_id="promptgen_generate", variant='primary')
                            with gr.Row():
                                gr.Markdown("# ")
                                    
        with contextlib.suppress(AttributeError):

            for i, dropdown_component in enumerate(dropdowns):
                all_none_button.click(none_dropdown_change, inputs=[dropdowns[i]], outputs=[dropdowns[i]])

            all_none_button.click(none_dropdown_change_clear, outputs=[auto_final])
            is_enabled.select(fn=lambda x:gr.update(label = f"🎨CreaPrompt : {'啟動' if x else '未啟動'}"),inputs=is_enabled, outputs=[acc])
            is_collection_enabled.select(fn=lambda x:gr.update(label = f"🎨CreaPrompt : {'啟動' if x else '未啟動'}"),inputs=is_collection_enabled, outputs=[acc])
            is_manual_enabled.select(fn=lambda x:gr.update(label = f"🎨CreaPrompt : {'啟動' if x else '未啟動'}"),inputs=is_manual_enabled, outputs=[acc])
            save_state_button_manu.click(save_checkbox_state_manu, inputs= [checkbox_group_manu, file_name_textbox_manu], outputs=[file_dropdown_component_manu, file_dropdown_component])
            save_state_button.click(save_checkbox_state, inputs= [checkbox_group, file_name_textbox], outputs=[file_dropdown_component, file_dropdown_component_manu])                        
            file_dropdown_component.change(load_checkbox_state, inputs=[file_dropdown_component], outputs=[checkbox_group])
            file_dropdown_component_manu.change(load_checkbox_state, inputs=[file_dropdown_component_manu], outputs=[checkbox_group_manu])
            is_collection_enabled.select(uncheck_auto_box, inputs=[is_collection_enabled, is_enabled, is_manual_enabled], outputs=[is_enabled, is_manual_enabled])
            is_enabled.select(uncheck_auto_collection, inputs=[is_enabled, is_collection_enabled, is_manual_enabled], outputs=[is_collection_enabled, is_manual_enabled])
            is_manual_enabled.select(uncheck_auto_manual, inputs=[is_manual_enabled, is_enabled, is_collection_enabled], outputs=[is_collection_enabled, is_enabled])

            for i, dropdown_component in enumerate(dropdowns):
                dropdown_component.select(lambda selected_value, index=i: handle_dropdown_change(selected_value, index), inputs=[dropdown_component], outputs=[auto_final])
                   
            if is_img2img:
                
                submit.click(
                           fn=read_random_line_from_csv_files_auto,
                           inputs=checkbox_group_manu,
                           outputs=prompt
                          )        
                Sendbefore.click(fn=send_before_prompt, inputs=[prompt, self.boxxIMG], outputs=[self.boxxIMG])
                Sendbefore.click(fn=send_before_prompt, inputs=[prompt, self.boxxIMG], outputs=[final])
                Sendafter.click(fn=send_after_prompt, inputs=[prompt, self.boxxIMG], outputs=[self.boxxIMG])
                Sendafter.click(fn=send_after_prompt, inputs=[prompt, self.boxxIMG], outputs=[final])
                send_text_button.click(fn=send_text_to_prompt, inputs=[prompt, self.boxxIMG, Prefix, sufix], outputs=[self.boxxIMG])
                send_text_button.click(fn=send_text_to_prompt, inputs=[prompt, self.boxxIMG, Prefix, sufix], outputs=[final])
                
            else:
                
                submit.click(
                           fn=read_random_line_from_csv_files_auto,
                           inputs=checkbox_group_manu,
                           outputs=prompt
                          )        
                Sendbefore.click(fn=send_before_prompt, inputs=[prompt, self.boxx], outputs=[self.boxx])
                Sendbefore.click(fn=send_before_prompt, inputs=[prompt, self.boxx], outputs=[final])
                Sendafter.click(fn=send_after_prompt, inputs=[prompt, self.boxx], outputs=[self.boxx])
                Sendafter.click(fn=send_after_prompt, inputs=[prompt, self.boxx], outputs=[final])
                send_text_button.click(fn=send_text_to_prompt, inputs=[prompt, self.boxx, Prefix, sufix], outputs=[self.boxx])
                send_text_button.click(fn=send_text_to_prompt, inputs=[prompt, self.boxx, Prefix, sufix], outputs=[final])
                
        return [is_enabled, checkbox_group, is_randomize, is_collection_enabled, prefix_auto, sufix_auto, is_randomize_manu, is_manual_enabled, is_manual_random, prefix_manual, sufix_manual]
        
    def process(self, p, is_enabled, checkbox_group, is_randomize, is_collection_enabled, prefix_auto, sufix_auto, is_randomize_manu, is_manual_enabled, is_manual_random, prefix_manual, sufix_manual):
    
        batchCount = len(p.all_prompts)
        
        if is_manual_enabled:
           if(batchCount == 1):
              back_dropdown_values = dropdown_values.copy()
              concatenated_values = ""
              values_exist = False
              for i, value in enumerate(back_dropdown_values):
                 if value:
                    values_exist = True
                    if value[0] == "🎲":
                       back_dropdown_values[i] = read_random_line_from_csv_file_manual(i)
              if not values_exist:  
                 p.all_prompts[0] = "請選擇類別"              
                 print("請選擇類別")   
              else:                 
                 for value in back_dropdown_values:
                    if value:
                       concatenated_values += value + ","
                 if prefix_manual:
                    concatenated_values = prefix_manual + "," + concatenated_values
                 if sufix_manual:
                    concatenated_values = concatenated_values + sufix_manual                      
                 concatenated_values = concatenated_values.rstrip(", ")
                 print("從類別中手動使用的提示：" + " " + concatenated_values)
                 p.extra_generation_params.update({"CreaPrompt":"從類別中手動"})
                 p.all_prompts[0] = concatenated_values
                 p.all_hr_prompts = p.all_prompts[0]
           if(batchCount > 1):   
              for i, prompt in enumerate(p.all_prompts):
                  if(is_manual_random):
                     back_dropdown_values = dropdown_values.copy()
                     concatenated_values = ""
                     values_exist = False
                     for a, value in enumerate(back_dropdown_values):
                        if value:
                           values_exist = True
                           if value[0] == "🎲":
                              back_dropdown_values[a] = read_random_line_from_csv_file_manual(a)
                     if not values_exist:  
                        p.all_prompts[i] = "請選擇類別"  
                        if i == 0:                        
                           print("請選擇類別")   
                     else:                 
                        for value in back_dropdown_values:
                           if value:
                              concatenated_values += value + ","
                        if prefix_manual:
                           concatenated_values = prefix_manual + "," + concatenated_values
                        if sufix_manual:
                           concatenated_values = concatenated_values + sufix_manual      
                        concatenated_values = concatenated_values.rstrip(", ")
                        print("從類別中手動使用的提示：" + " " + concatenated_values)
                        p.extra_generation_params.update({"CreaPrompt":"從類別中手動"})
                        p.all_prompts[i] = concatenated_values
                        p.all_hr_prompts = p.all_prompts[i]
                  else:
                   if i == 0:
                     back_dropdown_values = dropdown_values.copy()
                     concatenated_values = ""
                     values_exist = False
                     for a, value in enumerate(back_dropdown_values):
                        if value:
                           values_exist = True
                           if value[0] == "🎲":
                              back_dropdown_values[a] = read_random_line_from_csv_file_manual(a)
                     if not values_exist:  
                        concatenated_values = "請選擇類別"
                        print("請選擇類別")   
                     else:                 
                        for value in back_dropdown_values:
                           if value:
                              concatenated_values += value + ","
                        if prefix_manual:
                           concatenated_values = prefix_manual + "," + concatenated_values
                        if sufix_manual:
                           concatenated_values = concatenated_values + sufix_manual
                        concatenated_values = concatenated_values.rstrip(", ")
                        print("從類別中手動使用的提示：" + " " + concatenated_values)
                   p.extra_generation_params.update({"CreaPrompt":"從類別中手動"})
                   p.all_prompts[i] = concatenated_values
                   p.all_hr_prompts = p.all_prompts[i]
        if is_collection_enabled:
           if(batchCount == 1):
              for i, prompt in enumerate(p.all_prompts):
                  randprompt=select_random_line_from_collection()  
              p.all_prompts[i] = randprompt
              p.all_hr_prompts = p.all_prompts[i]
              print("從集合中使用的提示：" + " " + randprompt)    
              p.extra_generation_params.update({"CreaPrompt":"集合"})              
           if(batchCount > 1):
            randprompts = {}
            randprompt = ""
            for i, prompt in enumerate(p.all_prompts):
                if(is_randomize_manu):
                   randprompt = select_random_line_from_collection()
                   randprompts[i] = randprompt
                   p.all_prompts[i] = randprompts[i]
                   p.all_hr_prompts = p.all_prompts[i]
                   print("從集合中使用的提示：" + " " + randprompts[i])
                else:
                    if i == 0:
                      randprompt = select_random_line_from_collection()
                      print("從集合中使用的提示：" + " " + randprompt)
                p.all_prompts[i] = randprompt
                p.all_hr_prompts = p.all_prompts[i]                
                p.extra_generation_params.update({"CreaPrompt":"集合"})                
    
        if not is_enabled:
           return

        if(batchCount == 1):
            for i, prompt in enumerate(p.all_prompts):
                randprompt= read_random_line_from_csv_files(checkbox_group)
                if prefix_auto:
                   randprompt = prefix_auto + "," + randprompt
                if sufix_auto:
                   randprompt = randprompt + "," + randprompt
            p.all_prompts[i] = randprompt
            p.all_hr_prompts = p.all_prompts[i]
            print("從類別中隨機使用的提示：" + " " + randprompt)
            p.extra_generation_params.update({"CreaPrompt 隨機從類別":", ".join([str(x) for x in checkbox_group])})
            
        if(batchCount > 1):
            randprompts = {}
            randprompt = ""
            for i, prompt in enumerate(p.all_prompts):
                if(is_randomize):
                   randprompt = read_random_line_from_csv_files(checkbox_group)
                   if prefix_auto:
                      randprompt = prefix_auto + "," + randprompt
                   if sufix_auto:
                      randprompt = randprompt + "," + sufix_auto
                   randprompts[i] = randprompt
                   p.all_prompts[i] = randprompts[i]
                   p.all_hr_prompts = p.all_prompts[i]
                   print("從類別中隨機使用的提示：" + " " + randprompts[i])
                else:
                    if i == 0:
                      randprompt = read_random_line_from_csv_files(checkbox_group)
                      if prefix_auto:
                         randprompt = prefix_auto + "," + randprompt
                      if sufix_auto:
                         randprompt = randprompt + "," + randprompt
                      print("從類別中隨機使用的提示：" + " " + randprompt)
                p.all_prompts[i] = randprompt
                p.all_hr_prompts = p.all_prompts[i]
                p.extra_generation_params.update({"CreaPrompt 隨機從類別":", ".join([str(x) for x in checkbox_group])})

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG = component
