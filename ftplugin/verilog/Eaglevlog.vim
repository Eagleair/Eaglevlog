
nnoremap <buffer> ,i :call Generating_inst()<cr>
nnoremap <buffer> ,t :call Generating_tb()<cr>
nnoremap <buffer> ,e :call Shell_sim("")<CR>
nnoremap <buffer> ,r :call Shell_sim(" -clean")<CR>
:inoreab zh always @(*)<Enter>begin<Enter>if ()begin<Enter><Enter>end<Enter>else begin<Enter><Enter>end<Enter>end
:inoreab sx always @( posedge clk or negedge res_n ) begin<Enter>if() begin<Enter><Enter>end<Enter>else begin<Enter><Enter>end<Enter>end
:inoreab mk module <ESC>maa(<Enter><Enter>);<Enter>endmodule<ESC>`ai


let s:py_path = expand("<sfile>:h").'/../../py'
let b:bname = expand("%:r").'_tb.v'
py3	sys.path = [vim.eval("s:py_path")] + sys.path

function! Shell_sim(opt)
		" Get the bytecode.
	execute "normal! ma:cd %:h\<cr>gg/\\<module\\>\<cr>w"
	let model_tb = expand("<cword>")
	echo "执行仿真模块：".model_tb
	normal! `a

	silent !clear
	execute "! ".s:py_path."/vcs_sim.sh ".model_tb.a:opt

""		let bytecode = system("/home/ealge/Desktop/script/vcs_sim.sh ".model_tb.a:opt)
""		" Open a new split and set it up.
""		setlocal splitbelow
""		split _Shell_sim_
""		normal! ggdG
""		setlocal filetype=
""		setlocal buftype=nofile
""		setlocal bufhidden=hide
""		setlocal noswapfile
""		setlocal nobuflisted
""		setlocal nowrap
""
""		" Insert the bytecode.
""		call append(0, split(bytecode, '\v\n'))	
""		execute "normal! G\<C-l>"
""		nnoremap <buffer> q :q<CR>
endfunction
if exists("g:verilog_fun")
    finish
endif

let g:verilog_fun = "verilog"


function! Generating_inst()
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

