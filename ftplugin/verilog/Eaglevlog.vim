
nnoremap <buffer> ,i :call Generating_inst()<cr>
nnoremap <buffer> ,t :call Generating_tb()<cr>
:inoreab zh always @(*)<Enter>begin<Enter>if ()begin<Enter><Enter>end<Enter>else begin<Enter><Enter>end<Enter>end
:inoreab sx always @( posedge clk or negedge res_n ) begin<Enter>if() begin<Enter><Enter>end<Enter>else begin<Enter><Enter>end<Enter>end
:inoreab mk module <ESC>maa(<Enter><Enter>);<Enter>endmodule<ESC>`ai


let s:py_path = expand("<sfile>:h").'/../../py'
let b:bname = expand("%:r").'_tb.v'
py3	sys.path = [vim.eval("s:py_path")] + sys.path

if exists("g:verilog_fun")
    finish
endif

let g:verilog_fun = "verilog"

function! Generating_inst()
if exists("b:current_filetype")
    finish
endif
python3 << EOF
#!/usr/local/bin/python3
# -*- coding: UTF-8 -*- 

import vim
import module
from importlib import reload
reload(module)
cur=vim.current.buffer
with open(cur.name, "r") as f:
    f_str = f.read()
module_obj = module.Module()
cw = vim.current.window	# gets the current window
pos = cw.cursor		# gets a tuple (row, col)
cur.append(module_obj.get_inst(f_str).split('\n'),pos[0])
EOF
endfunction

function! Generating_tb()
if exists("b:current_filetype")
    finish
endif
python3 << EOF
#!/usr/local/bin/python3
# -*- coding: UTF-8 -*- 

import vim
import module
from importlib import reload
reload(module)
cur=vim.current.buffer
with open(cur.name, "r") as f:
    f_str = f.read()
module_obj = module.Module()
#module_obj.init_module(f_str)
vim.command("execute 'vsplit '.b:bname")
cur=vim.current.buffer
cur.append(module_obj.get_tb(f_str).split('\n'))
EOF
endfunction

