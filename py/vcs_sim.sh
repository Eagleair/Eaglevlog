#!/bin/bash -f

# Command line options
vlogan_opts="-full64"
vhdlan_opts="-full64"
vcs_elab_opts="-full64 -debug_pp -licqueue -l elaborate.log -cpp g++-4.8 -cc gcc-4.8 -LDFLAGS -Wl,--no-as-needed"
#vcs_elab_opts="-full64 -debug_pp -licqueue -l elaborate.log -LDFLAGS -Wl,--no-as-needed"
vcs_elab_api="/home/ealge/sortware/synopsys/verdi_2016.06-1/share/PLI/VCS/linux64/novas.tab \
	/home/ealge/sortware/synopsys/verdi_2016.06-1/share/PLI/VCS/linux64/pli.a"
vcs_sim_opts="-licqueue -l simulate.log"

# Design libraries
design_lib="my_lib"

# Simulation root library directory
sim_dir="vcs_sim"

# Compiled library path
lib_map_path="/home/my-linux/software/xilinx/compiled"

sim_tb=$1
sim_opt=$2
# Main steps
run()
{
  case $sim_opt in
    "-clean" )
      clean
      echo -e "---- start files are deleted ----\n"
      exit 0
    ;;
    * )
      echo -e "---- start create_lib_mappings ----\n"
      create_lib_mappings
      echo -e "---- start compile ----\n"
	  compile
      echo -e "---- start elaborate ----\n"
      elaborate
      echo -e "---- start simulate ----\n"
	  simulate
  esac
}

# RUN_STEP: <compile>
compile()
{
  # Compile design files
	vlogan -work $design_lib $vlogan_opts +v2k \
	-f verilog.f \
	2>&1 | tee -a vlogan.log
}

# RUN_STEP: <elaborate>
elaborate()
{
	vcs $vcs_elab_opts $design_lib.$sim_tb -o simv \
	-P $vcs_elab_api
}

# RUN_STEP: <simulate>
simulate()
{
  ./simv $vcs_sim_opts
#  verdi -f verilog.f -ssf counter_tb.fsdb -sswr novas_rc.rc -ssr my.session
	verdi -nologo -f verilog.f -ssf $sim_tb.fsdb -ssr ./verdiLog/novas_autosave.ses 1> verdi.log &
}

# Define design library mappings
create_lib_mappings()
{
	mkdir -pm 777 "$sim_dir/$design_lib"
	cd $sim_dir
	touch synopsys_sim.setup
	echo -e "$design_lib:$design_lib" > synopsys_sim.setup
#	echo -e "OTHERS=$lib_map_path/synopsys_sim.setup" >> synopsys_sim.setup
	find ./../ -maxdepth 1 -name "*.v" > verilog.f
}

# Delete generated data from the previous run
clean()
{
	# 删除除了verdiLog之外的所有文件，verdiLog文件保存.ses等布局文件
	cd vcs_sim && rm -rf `ls | grep -v -Fx verdiLog` && cd ..
}
# Launch script
run
