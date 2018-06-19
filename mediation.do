sem (fraccumulrevnew <- shock gini isrevertednew total_comment_na_replaced editis_per_neweditor_na_replaced log_numtotalrev fracreverted fracneweditor) (shock -> gini) (shock -> isrevertednew) (shock -> total_comment_na_replaced) (shock -> editis_per_neweditor_na_replaced)

nlcom [fraccumulrevnew]gini * [gini]shock
nlcom [fraccumulrevnew]isrevertednew * [isrevertednew]shock
nlcom [fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock
nlcom [fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock + ///
		[fraccumulrevnew]shock

		
sem (fraccumulrevnew <- shock gini isrevertednew total_comment_na_replaced editis_per_neweditor_na_replaced log_numtotalrev fracreverted fracneweditor) (shock -> gini) (shock -> isrevertednew) (shock -> total_comment_na_replaced) (shock -> editis_per_neweditor_na_replaced) if size_at_shock <= 3.555348
nlcom [fraccumulrevnew]gini * [gini]shock
nlcom [fraccumulrevnew]isrevertednew * [isrevertednew]shock
nlcom [fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock
nlcom [fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock + ///
		[fraccumulrevnew]shock

sem (fraccumulrevnew <- shock gini isrevertednew total_comment_na_replaced editis_per_neweditor_na_replaced log_numtotalrev fracreverted fracneweditor) (shock -> gini) (shock -> isrevertednew) (shock -> total_comment_na_replaced) (shock -> editis_per_neweditor_na_replaced) if size_at_shock > 3.555348
nlcom [fraccumulrevnew]gini * [gini]shock
nlcom [fraccumulrevnew]isrevertednew * [isrevertednew]shock
nlcom [fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock
nlcom [fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock

nlcom [fraccumulrevnew]gini * [gini]shock + ///
		[fraccumulrevnew]isrevertednew * [isrevertednew]shock + ///
		[fraccumulrevnew]total_comment_na_replaced * [total_comment_na_replaced]shock + ///
		[fraccumulrevnew]editis_per_neweditor_na_replaced * [editis_per_neweditor_na_replaced]shock + ///
		[fraccumulrevnew]shock
