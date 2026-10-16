
undefined1
FUN_00105680(uint *param_1,uint param_2,uint param_3,long param_4,long param_5,long *param_6,
            uint *param_7)

{
  uint *puVar1;
  uint *puVar2;
  char cVar3;
  byte bVar4;
  undefined1 uVar5;
  ulong uVar6;
  void *pvVar7;
  uint *puVar8;
  int *piVar9;
  byte bVar11;
  uint uVar12;
  long lVar13;
  undefined1 *puVar14;
  uint *puVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  long lVar19;
  uint uVar20;
  int iVar21;
  int iVar22;
  undefined8 *puVar23;
  char cVar24;
  uint uVar25;
  uint uVar26;
  undefined6 uVar27;
  undefined8 in_R10;
  int iVar28;
  long lVar29;
  uint uVar30;
  long in_FS_OFFSET;
  uint local_634;
  uint *local_628;
  long local_620;
  int local_610;
  uint local_60c;
  uint local_600;
  undefined4 local_5f8;
  undefined4 uStack_5f4;
  long *local_5f0;
  uint local_5e8 [20];
  undefined1 local_598 [16];
  undefined1 local_588 [16];
  undefined1 local_578 [16];
  undefined1 local_568 [16];
  int local_558 [2];
  long local_550 [17];
  uint local_4c8 [290];
  long local_40;
  int *piVar10;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  local_598 = (undefined1  [16])0x0;
  local_558[0] = 0;
  local_588 = (undefined1  [16])0x0;
  local_578 = (undefined1  [16])0x0;
  local_568 = (undefined1  [16])0x0;
  puVar15 = param_1;
  do {
    uVar30 = *puVar15;
    puVar15 = puVar15 + 1;
    *(int *)(local_598 + (ulong)uVar30 * 4) = *(int *)(local_598 + (ulong)uVar30 * 4) + 1;
  } while (puVar15 != param_1 + param_2);
  if (local_598._0_4_ == param_2) {
    pvVar7 = malloc(0x30);
    if (pvVar7 == (void *)0x0) {
LAB_00105d01:
      uVar5 = 3;
    }
    else {
      *(undefined8 *)((long)pvVar7 + 8) = 0;
      DAT_0012c440 = DAT_0012c440 + 3;
      *(undefined2 *)((long)pvVar7 + 0x10) = 0x163;
      *(undefined2 *)((long)pvVar7 + 0x20) = 0x163;
      *param_6 = (long)pvVar7 + 0x10;
      uVar5 = 0;
      *param_7 = 1;
    }
    goto LAB_00105d06;
  }
  lVar13 = 1;
  do {
    if (*(int *)(local_598 + lVar13 * 4) != 0) {
      local_60c = (uint)lVar13;
      iVar22 = 1 << ((byte)lVar13 & 0x1f);
      goto LAB_0010575b;
    }
    lVar13 = lVar13 + 1;
  } while (lVar13 != 0x11);
  local_60c = 0x11;
  iVar22 = 0x20000;
LAB_0010575b:
  uVar30 = *param_7;
  if (*param_7 < local_60c) {
    uVar30 = local_60c;
  }
  piVar9 = local_558;
  uVar16 = 0x10;
  do {
    if (*piVar9 != 0) {
      if (uVar16 < uVar30) {
        uVar30 = uVar16;
      }
      *param_7 = uVar30;
      local_634 = uVar16;
      if (uVar16 <= local_60c) goto LAB_001057a3;
      uVar6 = (ulong)local_60c;
      iVar22 = iVar22 - *(int *)(local_598 + uVar6 * 4);
      if (iVar22 < 0) goto LAB_00105d89;
      puVar14 = local_598 + uVar6 * 4;
      goto LAB_00105ad0;
    }
    piVar9 = piVar9 + -1;
    uVar16 = uVar16 - 1;
  } while (uVar16 != 0);
  *param_7 = 0;
  uVar30 = 0;
  local_634 = 0;
LAB_001057a3:
  iVar28 = iVar22 - *(int *)(local_598 + (ulong)uVar16 * 4);
  if (-1 < iVar28) {
    *(int *)(local_598 + (ulong)uVar16 * 4) = iVar22;
    local_5e8[1] = 0;
    if (uVar16 != 1) {
LAB_00105afb:
      uVar20 = 0;
      piVar9 = (int *)(local_598 + 4);
      puVar15 = local_5e8 + 2;
      do {
        piVar10 = piVar9 + 1;
        uVar20 = uVar20 + *piVar9;
        *puVar15 = uVar20;
        piVar9 = piVar10;
        puVar15 = puVar15 + 1;
      } while ((int *)(local_598 + (ulong)(uVar16 - 2) * 4 + 8) != piVar10);
    }
    local_5e8[1] = 0;
    uVar6 = 0;
    do {
      uVar16 = param_1[uVar6];
      if (uVar16 != 0) {
        uVar20 = local_5e8[uVar16];
        local_4c8[uVar20] = (uint)uVar6;
        local_5e8[uVar16] = uVar20 + 1;
      }
      uVar6 = uVar6 + 1;
    } while (param_2 != uVar6);
    local_550[1] = 0;
    iVar22 = -uVar30;
    local_5e8[0] = 0;
    if ((int)local_60c <= (int)local_634) {
      puVar15 = local_4c8;
      uVar20 = 0;
      puVar2 = puVar15 + local_5e8[(int)local_634];
      local_610 = -1;
      local_620 = CONCAT44(uStack_5f4,local_5f8);
      local_628 = (uint *)(local_598 + (long)(int)local_60c * 4);
      uVar16 = 0;
      lVar13 = 0;
      local_5f0 = param_6;
      do {
        local_600 = *local_628;
        if (local_600 != 0) {
          cVar3 = (char)local_60c;
          uVar17 = 1 << (cVar3 - 1U & 0x1f);
          do {
            iVar21 = uVar30 + iVar22;
            if (iVar21 < (int)local_60c) {
              uVar18 = local_60c - iVar21;
              uVar25 = local_634 - iVar21;
              lVar29 = (long)(local_610 + 1);
              do {
                iVar22 = iVar21;
                local_610 = (int)lVar29;
                bVar11 = (byte)uVar18;
                uVar20 = 1 << (bVar11 & 0x1f);
                uVar26 = uVar18;
                if (local_600 < uVar20) {
                  uVar12 = uVar30;
                  if (uVar25 <= uVar30) {
                    uVar12 = uVar25;
                  }
                  if (uVar18 < uVar12) {
                    uVar26 = uVar18 + 1;
                    iVar21 = uVar20 - local_600;
                    puVar8 = local_628;
                    if (uVar26 < uVar12) {
                      do {
                        puVar1 = puVar8 + 1;
                        puVar8 = puVar8 + 1;
                        if ((uint)(iVar21 * 2) <= *puVar1) break;
                        uVar26 = uVar26 + 1;
                        iVar21 = iVar21 * 2 - *puVar1;
                      } while (uVar26 != uVar12);
                    }
                    uVar20 = 1 << ((byte)uVar26 & 0x1f);
                  }
                }
                pvVar7 = malloc((ulong)(uVar20 + 1) << 4);
                if (pvVar7 == (void *)0x0) {
                  lVar13 = local_550[1];
                  if (local_610 != 0) {
                    while (lVar13 != 0) {
                      lVar29 = *(long *)(lVar13 + -8);
                      free((void *)(lVar13 + -0x10));
                      lVar13 = lVar29;
                    }
                  }
                  goto LAB_00105d01;
                }
                DAT_0012c440 = uVar20 + 1 + DAT_0012c440;
                lVar13 = (long)pvVar7 + 0x10;
                *local_5f0 = lVar13;
                local_5f0 = (long *)((long)pvVar7 + 8);
                *(undefined8 *)((long)pvVar7 + 8) = 0;
                local_550[lVar29 + 1] = lVar13;
                if (local_610 != 0) {
                  local_5e8[lVar29] = uVar16;
                  puVar23 = (undefined8 *)
                            (local_550[lVar29] +
                            (ulong)(uVar16 >> ((char)iVar22 - (char)uVar30 & 0x1fU)) * 0x10);
                  in_R10 = CONCAT62((int6)((ulong)in_R10 >> 0x10),
                                    CONCAT11((char)uVar30,(char)uVar26 + '\x10'));
                  puVar23[1] = lVar13;
                  *puVar23 = in_R10;
                  local_620 = lVar13;
                }
                lVar29 = lVar29 + 1;
                uVar25 = uVar25 - uVar30;
                uVar18 = uVar18 - uVar30;
                iVar21 = iVar22 + uVar30;
              } while ((int)(iVar22 + uVar30) < (int)local_60c);
            }
            else {
              bVar11 = cVar3 - (char)iVar22;
            }
            cVar24 = 'c';
            bVar4 = (byte)iVar22;
            if (puVar15 < puVar2) {
              uVar18 = *puVar15;
              puVar15 = puVar15 + 1;
              uVar27 = (undefined6)((ulong)local_620 >> 0x10);
              if (uVar18 < param_3) {
                local_620 = CONCAT62(uVar27,(short)uVar18);
                cVar24 = (uVar18 != 0x100) + '\x0f';
              }
              else {
                local_620 = CONCAT62(uVar27,*(undefined2 *)(param_4 + (ulong)(uVar18 - param_3) * 2)
                                    );
                cVar24 = *(char *)(param_5 + (ulong)(uVar18 - param_3) * 2);
              }
            }
            for (uVar18 = uVar16 >> (bVar4 & 0x1f); uVar18 < uVar20;
                uVar18 = uVar18 + (1 << (bVar11 & 0x1f))) {
              in_R10 = CONCAT62((int6)((ulong)in_R10 >> 0x10),CONCAT11(cVar3 - bVar4,cVar24));
              puVar23 = (undefined8 *)((ulong)uVar18 * 0x10 + lVar13);
              *puVar23 = in_R10;
              puVar23[1] = local_620;
            }
            uVar18 = uVar17 & uVar16;
            uVar25 = uVar17;
            while (uVar18 != 0) {
              uVar16 = uVar16 ^ uVar25;
              uVar25 = uVar25 >> 1;
              uVar18 = uVar16 & uVar25;
            }
            uVar16 = uVar16 ^ uVar25;
            if (((1 << (bVar4 & 0x1f)) - 1U & uVar16) != local_5e8[local_610]) {
              lVar29 = (long)(local_610 + -1);
              do {
                lVar19 = lVar29;
                iVar22 = iVar22 - uVar30;
                lVar29 = lVar19 + -1;
              } while (((1 << ((byte)iVar22 & 0x1f)) - 1U & uVar16) != local_5e8[lVar19]);
              local_610 = (int)lVar19;
            }
            local_600 = local_600 - 1;
          } while (local_600 != 0);
        }
        local_60c = local_60c + 1;
        local_628 = local_628 + 1;
      } while (local_634 + 1 != local_60c);
    }
    uVar5 = local_634 != 1 && iVar28 != 0;
    goto LAB_00105d06;
  }
  goto LAB_00105d89;
  while( true ) {
    iVar22 = iVar22 - *(int *)(puVar14 + 4);
    puVar14 = puVar14 + 4;
    if (iVar22 < 0) break;
LAB_00105ad0:
    iVar22 = iVar22 * 2;
    if (local_598 + (((uVar16 - local_60c) - 1) + uVar6) * 4 == puVar14) {
      iVar28 = iVar22 - *(int *)(local_598 + (ulong)uVar16 * 4);
      if (-1 < iVar28) {
        *(int *)(local_598 + (ulong)uVar16 * 4) = iVar22;
        local_5e8[1] = 0;
        goto LAB_00105afb;
      }
      break;
    }
  }
LAB_00105d89:
  uVar5 = 2;
LAB_00105d06:
  if (local_40 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar5;
}

