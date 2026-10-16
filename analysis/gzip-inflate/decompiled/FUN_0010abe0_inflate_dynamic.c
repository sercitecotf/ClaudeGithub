
uint FUN_0010abe0(void)

{
  void *pvVar1;
  ushort uVar2;
  ushort uVar3;
  char *pcVar4;
  undefined4 uVar5;
  byte bVar6;
  byte bVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  long lVar11;
  uint uVar12;
  long lVar13;
  uint uVar14;
  undefined8 *puVar15;
  uint uVar16;
  char *pcVar17;
  ulong uVar18;
  ulong uVar19;
  undefined4 *puVar20;
  uint uVar21;
  uint uVar22;
  uint *puVar23;
  ulong uVar24;
  long in_FS_OFFSET;
  byte bVar25;
  uint local_57c;
  uint local_564;
  undefined4 local_550;
  int local_54c;
  char *local_548;
  long local_540;
  uint local_538 [2];
  undefined1 auStack_530 [4];
  uint auStack_52c [315];
  long local_40;
  
  uVar5 = DAT_001df800;
  uVar18 = DAT_0012c438;
  uVar22 = DAT_0012c434;
  bVar25 = 0;
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  uVar21 = DAT_0012c434;
  if (DAT_0012c434 < 5) {
    uVar19 = (ulong)DAT_0016d90c;
    if (DAT_0016d90c < DAT_0016d908) {
      DAT_0016d90c = DAT_0016d90c + 1;
      bVar6 = (&DAT_0012d000)[uVar19];
    }
    else {
      bVar6 = FUN_00109360(0);
    }
    uVar21 = uVar22 + 8;
    uVar18 = uVar18 | (ulong)bVar6 << ((byte)uVar22 & 0x3f);
  }
  uVar22 = uVar21 - 5;
  uVar19 = uVar18 >> 5;
  uVar8 = ((uint)uVar18 & 0x1f) + 0x101;
  uVar14 = uVar22;
  if (uVar22 < 5) {
    uVar18 = (ulong)DAT_0016d90c;
    if (DAT_0016d90c < DAT_0016d908) {
      DAT_0016d90c = DAT_0016d90c + 1;
      bVar6 = (&DAT_0012d000)[uVar18];
    }
    else {
      DAT_001df800 = uVar5;
      bVar6 = FUN_00109360(0);
    }
    uVar14 = uVar21 + 3;
    uVar19 = uVar19 | (ulong)bVar6 << ((byte)uVar22 & 0x3f);
  }
  uVar22 = uVar14 - 5;
  uVar18 = uVar19 >> 5;
  uVar21 = ((uint)uVar19 & 0x1f) + 1;
  if (uVar22 < 4) {
    uVar19 = (ulong)DAT_0016d90c;
    if (DAT_0016d90c < DAT_0016d908) {
      DAT_0016d90c = DAT_0016d90c + 1;
      uVar18 = uVar18 | (ulong)(byte)(&DAT_0012d000)[uVar19] << ((byte)uVar22 & 0x3f);
      uVar22 = uVar14 + 3;
    }
    else {
      DAT_001df800 = uVar5;
      bVar6 = FUN_00109360(0);
      uVar18 = uVar18 | (ulong)bVar6 << ((byte)uVar22 & 0x3f);
      uVar22 = uVar14 + 3;
    }
  }
  if ((uVar8 < 0x11f) && (uVar21 < 0x1f)) {
    uVar22 = uVar22 - 4;
    uVar14 = (uint)uVar18 & 0xf;
    uVar19 = (ulong)uVar14;
    puVar23 = &DAT_00112aa0;
    uVar18 = uVar18 >> 4;
    do {
      uVar12 = uVar22;
      if (uVar22 < 3) {
        uVar24 = (ulong)DAT_0016d90c;
        if (DAT_0016d90c < DAT_0016d908) {
          DAT_0016d90c = DAT_0016d90c + 1;
          bVar6 = (&DAT_0012d000)[uVar24];
        }
        else {
          DAT_001df800 = uVar5;
          bVar6 = FUN_00109360(0);
        }
        uVar12 = uVar22 + 8;
        uVar18 = uVar18 | (ulong)bVar6 << ((byte)uVar22 & 0x3f);
      }
      uVar9 = *puVar23;
      uVar22 = uVar12 - 3;
      uVar24 = uVar18 >> 3;
      puVar23 = puVar23 + 1;
      local_538[uVar9] = (uint)uVar18 & 7;
      uVar18 = uVar24;
    } while ((uint *)(&DAT_00112ab0 + uVar19 * 4) != puVar23);
    if (uVar14 != 0xf) {
      puVar20 = &DAT_00112aa0 + uVar19;
      do {
        puVar23 = puVar20 + 4;
        puVar20 = puVar20 + 1;
        local_538[*puVar23] = 0;
      } while (puVar20 != &DAT_00112aa4 + (0xe - uVar14) + uVar19);
    }
    local_54c = 7;
    uVar14 = FUN_00105680(local_538,0x13,0x13,0,0,&local_540,&local_54c);
    lVar13 = local_540;
    if (uVar14 == 0) {
      if (local_540 == 0) goto LAB_0010b3c2;
      local_57c = 0;
      uVar18 = (ulong)local_54c;
      uVar14 = uVar8 + uVar21;
      local_564 = 0;
      uVar2 = *(ushort *)(&DAT_00112b00 + uVar18 * 2);
      do {
        uVar12 = uVar22;
        if (uVar22 < (uint)uVar18) {
          do {
            uVar19 = (ulong)DAT_0016d90c;
            if (DAT_0016d90c < DAT_0016d908) {
              DAT_0016d90c = DAT_0016d90c + 1;
              bVar6 = (&DAT_0012d000)[uVar19];
            }
            else {
              DAT_001df800 = uVar5;
              bVar6 = FUN_00109360(0);
            }
            uVar22 = uVar12 + 8;
            uVar24 = uVar24 | (ulong)bVar6 << ((byte)uVar12 & 0x3f);
            uVar12 = uVar22;
          } while (uVar22 < (uint)uVar18);
          uVar18 = uVar18 & 0xffffffff;
        }
        local_548 = (char *)((ulong)((uint)uVar2 & (uint)uVar24) * 0x10 + lVar13);
        uVar19 = uVar24 >> (local_548[1] & 0x3fU);
        uVar22 = uVar22 - (byte)local_548[1];
        if (*local_548 == 'c') goto LAB_0010b3b0;
        uVar3 = *(ushort *)(local_548 + 8);
        uVar12 = (uint)uVar3;
        if (uVar3 < 0x10) {
          lVar11 = (long)(int)local_564;
          local_564 = local_564 + 1;
          local_538[lVar11] = uVar12;
          uVar24 = uVar19;
          local_57c = uVar12;
        }
        else {
          bVar6 = (byte)uVar22;
          if (uVar3 == 0x10) {
            if (uVar22 < 2) {
              uVar24 = (ulong)DAT_0016d90c;
              if (DAT_0016d90c < DAT_0016d908) {
                DAT_0016d90c = DAT_0016d90c + 1;
                bVar7 = (&DAT_0012d000)[uVar24];
              }
              else {
                DAT_001df800 = uVar5;
                bVar7 = FUN_00109360(0);
              }
              uVar22 = uVar22 + 8;
              uVar19 = uVar19 | (ulong)bVar7 << (bVar6 & 0x3f);
            }
            uVar24 = uVar19 >> 2;
            uVar22 = uVar22 - 2;
            uVar12 = (uint)uVar19 & 3;
            if (uVar14 < uVar12 + 3 + local_564) goto LAB_0010ae2a;
            lVar11 = (long)(int)local_564;
            puVar23 = local_538 + lVar11;
            if (((int)(auStack_52c + (ulong)uVar12 + lVar11) - (int)puVar23 & 4U) == 0)
            goto LAB_0010b36e;
            *puVar23 = local_57c;
            for (puVar23 = local_538 + lVar11 + 1; puVar23 != auStack_52c + (ulong)uVar12 + lVar11;
                puVar23 = puVar23 + 2) {
LAB_0010b36e:
              *puVar23 = local_57c;
              puVar23[1] = local_57c;
            }
            local_564 = uVar12 + 3 + local_564;
          }
          else if (uVar12 == 0x11) {
            if (uVar22 < 3) {
              uVar24 = (ulong)DAT_0016d90c;
              if (DAT_0016d90c < DAT_0016d908) {
                DAT_0016d90c = DAT_0016d90c + 1;
                bVar7 = (&DAT_0012d000)[uVar24];
              }
              else {
                DAT_001df800 = uVar5;
                bVar7 = FUN_00109360(0);
              }
              uVar22 = uVar22 + 8;
              uVar19 = uVar19 | (ulong)bVar7 << (bVar6 & 0x3f);
            }
            uVar24 = uVar19 >> 3;
            uVar22 = uVar22 - 3;
            uVar12 = (uint)uVar19 & 7;
            if (uVar14 < uVar12 + 3 + local_564) goto LAB_0010ae2a;
            puVar23 = local_538 + (int)local_564;
            puVar23[0] = 0;
            puVar23[1] = 0;
            (puVar23 + ((ulong)(uVar12 + 3) - 2))[0] = 0;
            (puVar23 + ((ulong)(uVar12 + 3) - 2))[1] = 0;
            uVar9 = (uVar12 + 3) * 4 +
                    ((int)puVar23 -
                    (int)((ulong)(auStack_530 + (long)(int)local_564 * 4) & 0xfffffffffffffff8)) &
                    0xfffffff8;
            if (7 < uVar9) {
              uVar19 = 0;
              do {
                uVar16 = (int)uVar19 + 8;
                *(undefined8 *)
                 (((ulong)(auStack_530 + (long)(int)local_564 * 4) & 0xfffffffffffffff8) + uVar19) =
                     0;
                uVar19 = (ulong)uVar16;
              } while (uVar16 < uVar9);
            }
            local_57c = 0;
            local_564 = uVar12 + 3 + local_564;
          }
          else {
            if (uVar22 < 7) {
              uVar24 = (ulong)DAT_0016d90c;
              if (DAT_0016d90c < DAT_0016d908) {
                DAT_0016d90c = DAT_0016d90c + 1;
                bVar7 = (&DAT_0012d000)[uVar24];
              }
              else {
                DAT_001df800 = uVar5;
                bVar7 = FUN_00109360(0);
              }
              uVar22 = uVar22 + 8;
              uVar19 = uVar19 | (ulong)bVar7 << (bVar6 & 0x3f);
            }
            uVar24 = uVar19 >> 7;
            uVar22 = uVar22 - 7;
            uVar12 = (uint)uVar19 & 0x7f;
            if (uVar14 < uVar12 + 0xb + local_564) goto LAB_0010ae2a;
            lVar11 = (long)(int)local_564;
            local_564 = uVar12 + 0xb + local_564;
            puVar23 = local_538 + lVar11;
            puVar23[0] = 0;
            puVar23[1] = 0;
            (puVar23 + ((ulong)(uVar12 + 0xb) - 2))[0] = 0;
            (puVar23 + ((ulong)(uVar12 + 0xb) - 2))[1] = 0;
            puVar15 = (undefined8 *)((ulong)(auStack_530 + lVar11 * 4) & 0xfffffffffffffff8);
            for (uVar19 = (ulong)(((int)puVar23 -
                                  (int)(undefined8 *)
                                       ((ulong)(auStack_530 + lVar11 * 4) & 0xfffffffffffffff8)) +
                                  (uVar12 + 0xb) * 4 >> 3); uVar19 != 0; uVar19 = uVar19 - 1) {
              *puVar15 = 0;
              puVar15 = puVar15 + (ulong)bVar25 * -2 + 1;
            }
            local_57c = 0;
          }
        }
      } while (local_564 < uVar14);
      do {
        pvVar1 = (void *)(lVar13 + -0x10);
        lVar13 = *(long *)(lVar13 + -8);
        free(pvVar1);
      } while (lVar13 != 0);
      local_54c = 9;
      DAT_0012c434 = uVar22;
      DAT_0012c438 = uVar24;
      uVar14 = FUN_00105680(local_538,uVar8,0x101,&DAT_00117240,&DAT_00117200,&local_540,&local_54c)
      ;
      if (uVar14 == 0) {
        local_550 = 6;
        uVar14 = FUN_00105680(local_538 + uVar8,uVar21,0,&DAT_001171c0,&DAT_00117180,&local_548,
                              &local_550);
        pcVar17 = local_548;
        if (uVar14 == 0) {
          iVar10 = FUN_0010a3a0(local_540,local_548,local_54c,local_550);
          while (local_540 != 0) {
            pvVar1 = (void *)(local_540 + -0x10);
            local_540 = *(long *)(local_540 + -8);
            free(pvVar1);
          }
          while (pcVar17 != (char *)0x0) {
            pcVar4 = pcVar17 + -0x10;
            pcVar17 = *(char **)(pcVar17 + -8);
            free(pcVar4);
          }
          uVar14 = (uint)(iVar10 != 0);
        }
        else {
          if (uVar14 == 1) {
            while (pcVar17 != (char *)0x0) {
              pcVar4 = *(char **)(pcVar17 + -8);
              free(pcVar17 + -0x10);
              pcVar17 = pcVar4;
            }
          }
          while (local_540 != 0) {
            lVar13 = *(long *)(local_540 + -8);
            free((void *)(local_540 + -0x10));
            local_540 = lVar13;
          }
        }
        goto LAB_0010ae30;
      }
      if (uVar14 != 1) goto LAB_0010ae30;
      while (local_540 != 0) {
        lVar13 = *(long *)(local_540 + -8);
        free((void *)(local_540 + -0x10));
        local_540 = lVar13;
      }
    }
    else {
      if (uVar14 != 1) goto LAB_0010ae30;
      while (local_540 != 0) {
        lVar13 = *(long *)(local_540 + -8);
        free((void *)(local_540 + -0x10));
        local_540 = lVar13;
      }
    }
  }
LAB_0010ae2a:
  uVar14 = 1;
LAB_0010ae30:
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return uVar14;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
LAB_0010b3b0:
  do {
    pvVar1 = (void *)(lVar13 + -0x10);
    lVar13 = *(long *)(lVar13 + -8);
    free(pvVar1);
  } while (lVar13 != 0);
LAB_0010b3c2:
  uVar14 = 2;
  goto LAB_0010ae30;
}

