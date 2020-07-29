; ModuleID = 'libjit.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: alwaysinline nofree norecurse nounwind
define i32 @linear_34b_v1(i8*, i8*, i8* nocapture readnone) local_unnamed_addr #0 {
entry:
  %3 = ptrtoint i8* %0 to i64
  %4 = ptrtoint i8* %1 to i64
  %5 = add i64 %4, 192
  %6 = inttoptr i64 %5 to float*
  %7 = bitcast i8* %1 to float*
  %8 = add i64 %3, 64
  %9 = inttoptr i64 %8 to float*
  tail call fastcc void @libjit_matmul_f_0_specialized(float* %6, float* %7, float* %9) #2
  %10 = bitcast i8* %0 to float*
  tail call fastcc void @libjit_batchedadd_f_1_specialized(float* %6, float* %6, float* %10) #2
  ret i32 0
}

; Function Attrs: nofree noinline norecurse nounwind
define internal fastcc void @libjit_matmul_f_0_specialized(float* nocapture, float* nocapture readonly, float* nocapture readonly) unnamed_addr #1 {
.preheader.lr.ph.i1.i.i.preheader:
  %3 = bitcast float* %0 to i32*
  store i32 0, i32* %3, align 4
  br label %.preheader.lr.ph.i1.i.i

.preheader.lr.ph.i1.i.i:                          ; preds = %.preheader.lr.ph.i1.i.i.1, %.preheader.lr.ph.i1.i.i.preheader
  %4 = phi float [ 0.000000e+00, %.preheader.lr.ph.i1.i.i.preheader ], [ %28, %.preheader.lr.ph.i1.i.i.1 ]
  %indvars.iv15.i.i.i = phi i64 [ 0, %.preheader.lr.ph.i1.i.i.preheader ], [ %indvars.iv.next16.i.i.i.1.1, %.preheader.lr.ph.i1.i.i.1 ]
  %5 = getelementptr inbounds float, float* %2, i64 %indvars.iv15.i.i.i
  %6 = getelementptr inbounds float, float* %1, i64 %indvars.iv15.i.i.i
  %7 = load float, float* %5, align 4
  %8 = load float, float* %6, align 4
  %9 = fmul reassoc nsz arcp contract float %7, %8
  %10 = fadd reassoc nsz arcp contract float %4, %9
  store float %10, float* %0, align 4
  %indvars.iv.next16.i.i.i = or i64 %indvars.iv15.i.i.i, 1
  %11 = getelementptr inbounds float, float* %2, i64 %indvars.iv.next16.i.i.i
  %12 = getelementptr inbounds float, float* %1, i64 %indvars.iv.next16.i.i.i
  %13 = load float, float* %11, align 4
  %14 = load float, float* %12, align 4
  %15 = fmul reassoc nsz arcp contract float %13, %14
  %16 = fadd reassoc nsz arcp contract float %10, %15
  store float %16, float* %0, align 4
  %indvars.iv.next16.i.i.i.1 = or i64 %indvars.iv15.i.i.i, 2
  %exitcond18.i.i.i.1 = icmp eq i64 %indvars.iv.next16.i.i.i.1, 34
  br i1 %exitcond18.i.i.i.1, label %._crit_edge28.i, label %.preheader.lr.ph.i1.i.i.1

._crit_edge28.i:                                  ; preds = %.preheader.lr.ph.i1.i.i
  ret void

.preheader.lr.ph.i1.i.i.1:                        ; preds = %.preheader.lr.ph.i1.i.i
  %17 = getelementptr inbounds float, float* %2, i64 %indvars.iv.next16.i.i.i.1
  %18 = getelementptr inbounds float, float* %1, i64 %indvars.iv.next16.i.i.i.1
  %19 = load float, float* %17, align 4
  %20 = load float, float* %18, align 4
  %21 = fmul reassoc nsz arcp contract float %19, %20
  %22 = fadd reassoc nsz arcp contract float %16, %21
  store float %22, float* %0, align 4
  %indvars.iv.next16.i.i.i.12 = or i64 %indvars.iv15.i.i.i, 3
  %23 = getelementptr inbounds float, float* %2, i64 %indvars.iv.next16.i.i.i.12
  %24 = getelementptr inbounds float, float* %1, i64 %indvars.iv.next16.i.i.i.12
  %25 = load float, float* %23, align 4
  %26 = load float, float* %24, align 4
  %27 = fmul reassoc nsz arcp contract float %25, %26
  %28 = fadd reassoc nsz arcp contract float %22, %27
  store float %28, float* %0, align 4
  %indvars.iv.next16.i.i.i.1.1 = add nuw nsw i64 %indvars.iv15.i.i.i, 4
  br label %.preheader.lr.ph.i1.i.i
}

; Function Attrs: nofree noinline norecurse nounwind
define internal fastcc void @libjit_batchedadd_f_1_specialized(float* nocapture, float* nocapture readonly, float* nocapture readonly) unnamed_addr #1 {
.preheader:
  %3 = load float, float* %1, align 4
  %4 = load float, float* %2, align 4
  %5 = fadd reassoc nsz arcp contract float %3, %4
  store float %5, float* %0, align 4
  ret void
}

attributes #0 = { alwaysinline nofree norecurse nounwind "no-frame-pointer-elim"="true" }
attributes #1 = { nofree noinline norecurse nounwind "no-frame-pointer-elim"="true" }
attributes #2 = { nounwind }

!llvm.ident = !{!0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3}

!0 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
!1 = !{i32 2, !"Dwarf Version", i32 4}
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 4}
