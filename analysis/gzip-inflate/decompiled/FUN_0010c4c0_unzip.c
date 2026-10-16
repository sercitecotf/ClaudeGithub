
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0010c4c0(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;
  undefined1 uVar2;
  byte bVar3;
  byte bVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  ulong uVar8;
  ulong uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  undefined4 uVar13;
  uint *puVar14;
  uint *puVar15;
  uint uVar16;
  ulong uVar17;
  ulong uVar18;
  long in_FS_OFFSET;
  bool bVar19;
  uint local_74;
  ulong local_68;
  int local_60;
  uint local_58;
  uint local_54;
  uint local_50;
  uint local_4c;
  uint local_48 [2];
  long local_40;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  DAT_00117288 = 0xffffffff;
  DAT_0016d458 = param_1;
  DAT_0019e008 = param_2;
  if (DAT_0012c880 == 0) {
    if (DAT_00117294 != 8) {
LAB_0010c8a9:
                    /* WARNING: Subroutine does not return */
      FUN_00108650("internal error, invalid method");
    }
    uVar1 = 0;
    local_68 = 0;
LAB_0010c5f9:
    DAT_001df800 = 0;
    DAT_0012c434 = 0;
    DAT_0012c438 = 0;
    do {
      uVar17 = DAT_0012c438;
      uVar12 = DAT_0012c434;
      DAT_0012c440 = 0;
      uVar16 = (uint)DAT_0012c438;
      if (DAT_0012c434 == 0) {
        uVar8 = (ulong)DAT_0016d90c;
        if (DAT_0016d90c < DAT_0016d908) {
          DAT_0016d90c = DAT_0016d90c + 1;
          bVar3 = (&DAT_0012d000)[uVar8];
        }
        else {
          bVar3 = FUN_00109360(0);
        }
        uVar12 = 5;
        uVar8 = (bVar3 | uVar17) >> 1;
        uVar17 = (ulong)((bVar3 | uVar16) & 1);
      }
      else {
        uVar5 = DAT_0012c434 - 1;
        uVar8 = DAT_0012c438 >> 1;
        uVar17 = (ulong)(uVar16 & 1);
        if (uVar5 < 2) {
          uVar18 = (ulong)DAT_0016d90c;
          if (DAT_0016d90c < DAT_0016d908) {
            DAT_0016d90c = DAT_0016d90c + 1;
            bVar3 = (&DAT_0012d000)[uVar18];
          }
          else {
            bVar3 = FUN_00109360(0);
          }
          uVar12 = uVar12 + 5;
          uVar8 = uVar8 | (ulong)bVar3 << ((byte)uVar5 & 0x3f);
        }
        else {
          uVar12 = DAT_0012c434 - 3;
        }
      }
      uVar16 = DAT_001df800;
      DAT_0012c438 = uVar8 >> 2;
      uVar5 = (uint)uVar8 & 3;
      DAT_0012c434 = uVar12;
      if (uVar5 == 2) {
        iVar7 = FUN_0010abe0();
LAB_0010cb75:
        if (iVar7 != 0) {
          if (iVar7 != 3) {
LAB_0010c69e:
                    /* WARNING: Subroutine does not return */
            FUN_00108650("invalid compressed data--format violated");
          }
          FUN_001089c0();
          goto LAB_0010ccc1;
        }
      }
      else {
        if ((uVar8 & 3) != 0) {
          if (uVar5 != 1) goto LAB_0010c69e;
          iVar7 = FUN_0010a9e0();
          goto LAB_0010cb75;
        }
        uVar8 = (ulong)DAT_001df800;
        uVar6 = uVar12 & 7;
        uVar5 = uVar12 - uVar6;
        uVar18 = DAT_0012c438 >> (sbyte)uVar6;
        uVar10 = uVar5;
        if (uVar5 < 0x10) {
          do {
            while( true ) {
              uVar9 = (ulong)DAT_0016d90c;
              if (DAT_0016d90c < DAT_0016d908) break;
              DAT_001df800 = uVar16;
              bVar3 = FUN_00109360(0);
              uVar11 = uVar10 + 8;
              uVar18 = uVar18 | (ulong)bVar3 << ((byte)uVar10 & 0x3f);
              uVar10 = uVar11;
              if (0xf < uVar11) goto LAB_0010c9ce;
            }
            DAT_0016d90c = DAT_0016d90c + 1;
            uVar11 = uVar10 + 8;
            uVar18 = uVar18 | (ulong)(byte)(&DAT_0012d000)[uVar9] << ((byte)uVar10 & 0x3f);
            uVar10 = uVar11;
          } while (uVar11 < 0x10);
LAB_0010c9ce:
          local_74 = (uint)uVar18 & 0xffff;
          uVar18 = uVar18 >> 0x10;
          uVar5 = uVar5 + 8 + ((uVar6 - uVar12) + 0xf & 0xfffffff8);
          uVar12 = uVar5 - 0x10;
          uVar10 = uVar12;
LAB_0010ca13:
          do {
            while( true ) {
              uVar9 = (ulong)DAT_0016d90c;
              bVar3 = (byte)uVar12;
              if (DAT_0016d90c < DAT_0016d908) break;
              DAT_001df800 = uVar16;
              bVar4 = FUN_00109360(0);
              uVar12 = uVar12 + 8;
              uVar18 = uVar18 | (ulong)bVar4 << (bVar3 & 0x3f);
              if (0xf < uVar12) goto LAB_0010ca4e;
            }
            DAT_0016d90c = DAT_0016d90c + 1;
            uVar12 = uVar12 + 8;
            uVar18 = uVar18 | (ulong)(byte)(&DAT_0012d000)[uVar9] << (bVar3 & 0x3f);
          } while (uVar12 < 0x10);
LAB_0010ca4e:
          uVar12 = (0x1f - uVar5 & 0xfffffff8) + 8 + uVar10;
        }
        else {
          local_74 = (uint)uVar18 & 0xffff;
          uVar12 = uVar5 - 0x10;
          uVar18 = uVar18 >> 0x10;
          uVar10 = uVar12;
          if (uVar12 < 0x10) goto LAB_0010ca13;
        }
        if ((~(uint)uVar18 & 0xffff) != local_74) goto LAB_0010c69e;
        uVar18 = uVar18 >> 0x10;
        local_60 = local_74 - 1;
        uVar12 = uVar12 - 0x10;
        if (local_74 != 0) {
          do {
            while( true ) {
              if (uVar12 < 8) {
                uVar9 = (ulong)DAT_0016d90c;
                if (DAT_0016d90c < DAT_0016d908) {
                  DAT_0016d90c = DAT_0016d90c + 1;
                  uVar18 = uVar18 | (ulong)(byte)(&DAT_0012d000)[uVar9] << ((byte)uVar12 & 0x3f);
                }
                else {
                  DAT_001df800 = (int)uVar8;
                  bVar3 = FUN_00109360(0);
                  uVar18 = uVar18 | (ulong)bVar3 << ((byte)uVar12 & 0x3f);
                }
              }
              else {
                uVar12 = uVar12 - 8;
              }
              uVar16 = (int)uVar8 + 1;
              (&DAT_0018e000)[uVar8] = (char)uVar18;
              if (uVar16 == 0x8000) break;
              local_60 = local_60 + -1;
              uVar18 = uVar18 >> 8;
              uVar8 = (ulong)uVar16;
              if (local_60 == -1) goto LAB_0010cc06;
            }
            DAT_001df800 = 0x8000;
            uVar18 = uVar18 >> 8;
            FUN_001092e0();
            local_60 = local_60 + -1;
            uVar8 = 0;
          } while (local_60 != -1);
        }
LAB_0010cc06:
        DAT_001df800 = (uint)uVar8;
        DAT_0012c434 = uVar12;
        DAT_0012c438 = uVar18;
      }
    } while ((int)uVar17 == 0);
    if (7 < DAT_0012c434) {
      uVar12 = DAT_0012c434 - 8;
      DAT_0012c434 = DAT_0012c434 & 7;
      DAT_0016d90c = DAT_0016d90c + ~(uVar12 >> 3);
    }
  }
  else {
    if (DAT_0012c884 == 0) {
      local_68 = (ulong)DAT_0012d00e;
      uVar1 = DAT_0012d016;
    }
    else {
      local_68 = 0;
      uVar1 = 0;
    }
    if (DAT_00117294 == 8) goto LAB_0010c5f9;
    if (DAT_00117294 != 0) goto LAB_0010c8a9;
    uVar8 = (ulong)DAT_0012d012;
    uVar17 = (ulong)DAT_0012d016;
    if (DAT_0012c888 != 0) {
      uVar8 = uVar8 - 0xc;
    }
    if (uVar17 != uVar8) {
LAB_0010ccc1:
      FUN_00108460(_stderr,"len %lu, siz %lu\n",uVar17);
                    /* WARNING: Subroutine does not return */
      FUN_00108650("invalid compressed data--length mismatch");
    }
    for (; uVar17 != 0; uVar17 = uVar17 - 1) {
      while( true ) {
        uVar8 = (ulong)DAT_0016d90c;
        if (DAT_0016d90c < DAT_0016d908) {
          DAT_0016d90c = DAT_0016d90c + 1;
          uVar2 = (&DAT_0012d000)[uVar8];
        }
        else {
          uVar2 = FUN_00109360(0);
        }
        uVar8 = (ulong)DAT_001df800;
        DAT_001df800 = DAT_001df800 + 1;
        (&DAT_0018e000)[uVar8] = uVar2;
        if (DAT_001df800 == 0x8000) break;
        uVar17 = uVar17 - 1;
        if (uVar17 == 0) goto LAB_0010c6d0;
      }
      FUN_001092e0();
    }
  }
LAB_0010c6d0:
  FUN_001092e0();
  if (DAT_0012c880 == 0) {
    puVar15 = &local_58;
    do {
      while (uVar17 = (ulong)DAT_0016d90c, DAT_0016d90c < DAT_0016d908) {
        DAT_0016d90c = DAT_0016d90c + 1;
        puVar14 = (uint *)((long)puVar15 + 1);
        *(undefined1 *)puVar15 = (&DAT_0012d000)[uVar17];
        puVar15 = puVar14;
        if (&local_50 == puVar14) goto LAB_0010c73c;
      }
      puVar14 = (uint *)((long)puVar15 + 1);
      uVar2 = FUN_00109360(0);
      *(undefined1 *)puVar15 = uVar2;
      puVar15 = puVar14;
    } while (&local_50 != puVar14);
LAB_0010c73c:
    local_68 = (ulong)local_58;
    uVar1 = local_54;
  }
  else if (DAT_0012c884 != 0) {
    puVar15 = &local_58;
    do {
      while (uVar17 = (ulong)DAT_0016d90c, DAT_0016d90c < DAT_0016d908) {
        DAT_0016d90c = DAT_0016d90c + 1;
        puVar14 = (uint *)((long)puVar15 + 1);
        *(undefined1 *)puVar15 = (&DAT_0012d000)[uVar17];
        puVar15 = puVar14;
        if (local_48 == puVar14) goto LAB_0010c91c;
      }
      puVar14 = (uint *)((long)puVar15 + 1);
      uVar2 = FUN_00109360(0);
      *(undefined1 *)puVar15 = uVar2;
      puVar15 = puVar14;
    } while (local_48 != puVar14);
LAB_0010c91c:
    local_68 = (ulong)local_54;
    uVar1 = local_4c;
  }
  bVar19 = local_68 != (DAT_00117288 ^ 0xffffffff);
  if (bVar19) {
    FUN_00108460(_stderr,"\n%s: %s: invalid compressed data--crc error\n",DAT_0016de00,&DAT_0016d9a0
                );
  }
  if ((uint)DAT_0016d450 == uVar1) {
    if (DAT_0012c880 != 0) goto LAB_0010c7d7;
LAB_0010c838:
    DAT_0012c880 = 0;
    uVar13 = 0;
    if (!bVar19) goto LAB_0010c878;
  }
  else {
    FUN_00108460(_stderr,"\n%s: %s: invalid compressed data--length error\n",DAT_0016de00,
                 &DAT_0016d9a0);
    if (DAT_0012c880 != 0) {
      bVar19 = true;
LAB_0010c7d7:
      if ((DAT_0016d90c + 4 < DAT_0016d908) &&
         (((long)(int)(uint)*(ushort *)(&DAT_0012d002 + DAT_0016d90c) << 0x10 |
          (long)(int)(uint)*(ushort *)(&DAT_0012d000 + DAT_0016d90c)) == 0x4034b50)) {
        if (DAT_0016ddd0 == 0) {
          FUN_00108460(_stderr,"%s: %s has more than one entry -- unchanged\n",DAT_0016de00,
                       &DAT_0016d9a0);
          DAT_0012c880 = 0;
          goto LAB_0010c85b;
        }
        if (DAT_0016ddd8 == 0) {
          FUN_00108460(_stderr,"%s: %s has more than one entry--rest ignored\n",DAT_0016de00,
                       &DAT_0016d9a0);
        }
        if (DAT_0016ddf8 == 0) {
          DAT_0016ddf8 = 2;
        }
      }
      goto LAB_0010c838;
    }
  }
LAB_0010c85b:
  DAT_0012c868 = local_68;
  DAT_0012c884 = 0;
  DAT_0016ddf8 = 1;
  if (DAT_0016ddc0 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00105610();
  }
  uVar13 = 1;
LAB_0010c878:
  DAT_0012c868 = local_68;
  DAT_0012c884 = 0;
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return uVar13;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

