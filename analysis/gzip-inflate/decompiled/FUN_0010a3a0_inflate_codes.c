
undefined8 FUN_0010a3a0(long param_1,long param_2,uint param_3,uint param_4)

{
  uint uVar1;
  ushort uVar2;
  ushort uVar3;
  ushort uVar4;
  ushort uVar5;
  byte bVar6;
  byte bVar7;
  ulong uVar8;
  ulong uVar9;
  ulong uVar10;
  uint uVar11;
  int iVar12;
  byte *pbVar13;
  uint uVar14;
  uint uVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  
  uVar2 = *(ushort *)(&DAT_00112b00 + (long)(int)param_3 * 2);
  uVar3 = *(ushort *)(&DAT_00112b00 + (long)(int)param_4 * 2);
  uVar10 = DAT_0012c438;
  uVar11 = DAT_0012c434;
  uVar16 = DAT_001df800;
  do {
    while( true ) {
      for (; uVar11 < param_3; uVar11 = uVar11 + 8) {
        uVar8 = (ulong)DAT_0016d90c;
        if (DAT_0016d90c < DAT_0016d908) {
          DAT_0016d90c = DAT_0016d90c + 1;
          bVar7 = (&DAT_0012d000)[uVar8];
        }
        else {
          DAT_001df800 = uVar16;
          bVar7 = FUN_00109360(0);
        }
        uVar10 = uVar10 | (ulong)bVar7 << ((byte)uVar11 & 0x3f);
      }
      pbVar13 = (byte *)((ulong)((uint)uVar2 & (uint)uVar10) * 0x10 + param_1);
      bVar7 = *pbVar13;
      while (0x10 < bVar7) {
        if (bVar7 == 99) {
          return 1;
        }
        uVar15 = bVar7 - 0x10;
        uVar10 = uVar10 >> (pbVar13[1] & 0x3f);
        for (uVar11 = uVar11 - pbVar13[1]; uVar11 < uVar15; uVar11 = uVar11 + 8) {
          uVar8 = (ulong)DAT_0016d90c;
          if (DAT_0016d90c < DAT_0016d908) {
            DAT_0016d90c = DAT_0016d90c + 1;
            bVar7 = (&DAT_0012d000)[uVar8];
          }
          else {
            DAT_001df800 = uVar16;
            bVar7 = FUN_00109360(0);
          }
          uVar10 = uVar10 | (ulong)bVar7 << ((byte)uVar11 & 0x3f);
        }
        pbVar13 = (byte *)((ulong)((uint)*(ushort *)(&DAT_00112b00 + (ulong)uVar15 * 2) &
                                  (uint)uVar10) * 0x10 + *(long *)(pbVar13 + 8));
        bVar7 = *pbVar13;
      }
      uVar11 = uVar11 - pbVar13[1];
      uVar10 = uVar10 >> (pbVar13[1] & 0x3f);
      uVar15 = (uint)bVar7;
      if (uVar15 != 0x10) break;
      uVar8 = (ulong)uVar16;
      uVar16 = uVar16 + 1;
      (&DAT_0018e000)[uVar8] = (char)*(undefined2 *)(pbVar13 + 8);
      if (uVar16 == 0x8000) {
        DAT_001df800 = 0x8000;
        FUN_001092e0();
        uVar16 = 0;
      }
    }
    if (uVar15 == 0xf) {
      DAT_001df800 = uVar16;
      DAT_0012c438 = uVar10;
      DAT_0012c434 = uVar11;
      return 0;
    }
    if (uVar11 < uVar15) {
      do {
        uVar18 = uVar11;
        uVar8 = (ulong)DAT_0016d90c;
        if (DAT_0016d90c < DAT_0016d908) {
          DAT_0016d90c = DAT_0016d90c + 1;
          uVar8 = (ulong)(byte)(&DAT_0012d000)[uVar8] << ((byte)uVar18 & 0x3f);
        }
        else {
          DAT_001df800 = uVar16;
          bVar6 = FUN_00109360(0);
          uVar8 = (ulong)bVar6 << ((byte)uVar18 & 0x3f);
        }
        uVar10 = uVar10 | uVar8;
        uVar11 = uVar18 + 8;
      } while (uVar18 + 8 < uVar15);
      uVar11 = uVar18 + 8;
    }
    uVar4 = *(ushort *)(pbVar13 + 8);
    uVar11 = uVar11 - uVar15;
    uVar8 = uVar10 >> (bVar7 & 0x3f);
    uVar5 = *(ushort *)(&DAT_00112b00 + (ulong)bVar7 * 2);
    if (uVar11 < param_4) {
      do {
        while( true ) {
          uVar15 = uVar11;
          uVar9 = (ulong)DAT_0016d90c;
          if (DAT_0016d90c < DAT_0016d908) break;
          DAT_001df800 = uVar16;
          bVar7 = FUN_00109360(0);
          uVar8 = uVar8 | (ulong)bVar7 << ((byte)uVar15 & 0x3f);
          uVar11 = uVar15 + 8;
          if (param_4 <= uVar15 + 8) goto LAB_0010a5bb;
        }
        DAT_0016d90c = DAT_0016d90c + 1;
        uVar8 = uVar8 | (ulong)(byte)(&DAT_0012d000)[uVar9] << ((byte)uVar15 & 0x3f);
        uVar11 = uVar15 + 8;
      } while (uVar15 + 8 < param_4);
LAB_0010a5bb:
      uVar11 = uVar15 + 8;
    }
    pbVar13 = (byte *)((ulong)((uint)uVar3 & (uint)uVar8) * 0x10 + param_2);
    uVar15 = (uint)*pbVar13;
    if (0x10 < *pbVar13) {
      do {
        if (uVar15 == 99) {
          return 1;
        }
        uVar15 = uVar15 - 0x10;
        uVar11 = uVar11 - pbVar13[1];
        uVar8 = uVar8 >> (pbVar13[1] & 0x3f);
        if (uVar11 < uVar15) {
          do {
            while( true ) {
              uVar18 = uVar11;
              uVar9 = (ulong)DAT_0016d90c;
              if (DAT_0016d90c < DAT_0016d908) break;
              DAT_001df800 = uVar16;
              bVar7 = FUN_00109360(0);
              uVar8 = uVar8 | (ulong)bVar7 << ((byte)uVar18 & 0x3f);
              uVar11 = uVar18 + 8;
              if (uVar15 <= uVar18 + 8) goto LAB_0010a686;
            }
            DAT_0016d90c = DAT_0016d90c + 1;
            uVar8 = uVar8 | (ulong)(byte)(&DAT_0012d000)[uVar9] << ((byte)uVar18 & 0x3f);
            uVar11 = uVar18 + 8;
          } while (uVar18 + 8 < uVar15);
LAB_0010a686:
          uVar11 = uVar18 + 8;
        }
        pbVar13 = (byte *)((ulong)((uint)*(ushort *)(&DAT_00112b00 + (ulong)uVar15 * 2) &
                                  (uint)uVar8) * 0x10 + *(long *)(pbVar13 + 8));
        uVar15 = (uint)*pbVar13;
      } while (0x10 < uVar15);
    }
    uVar11 = uVar11 - pbVar13[1];
    uVar8 = uVar8 >> (pbVar13[1] & 0x3f);
    if (uVar11 < uVar15) {
      do {
        while( true ) {
          uVar18 = uVar11;
          uVar9 = (ulong)DAT_0016d90c;
          if (DAT_0016d90c < DAT_0016d908) break;
          DAT_001df800 = uVar16;
          bVar7 = FUN_00109360(0);
          uVar8 = uVar8 | (ulong)bVar7 << ((byte)uVar18 & 0x3f);
          uVar11 = uVar18 + 8;
          if (uVar15 <= uVar18 + 8) goto LAB_0010a75d;
        }
        DAT_0016d90c = DAT_0016d90c + 1;
        uVar8 = uVar8 | (ulong)(byte)(&DAT_0012d000)[uVar9] << ((byte)uVar18 & 0x3f);
        uVar11 = uVar18 + 8;
      } while (uVar18 + 8 < uVar15);
LAB_0010a75d:
      uVar11 = uVar18 + 8;
    }
    uVar11 = uVar11 - uVar15;
    uVar9 = (ulong)uVar16;
    uVar18 = ((uint)uVar5 & (uint)uVar10) + (uint)uVar4;
    uVar10 = uVar8 >> ((byte)uVar15 & 0x3f);
    uVar16 = (uVar16 - *(ushort *)(pbVar13 + 8)) -
             ((uint)*(ushort *)(&DAT_00112b00 + (ulong)uVar15 * 2) & (uint)uVar8);
    do {
      while( true ) {
        uVar15 = uVar16 & 0x7fff;
        uVar14 = (uint)uVar9;
        if (uVar15 <= uVar14) break;
        uVar17 = 0x8000 - uVar15;
        if (uVar18 < 0x8000 - uVar15) {
          uVar17 = uVar18;
        }
        uVar18 = uVar18 - uVar17;
LAB_0010a7cd:
        if (uVar17 <= uVar15 - uVar14) goto LAB_0010a7d8;
LAB_0010a850:
        uVar16 = uVar15 + uVar17;
        iVar12 = uVar14 - uVar15;
        do {
          uVar8 = (ulong)uVar15;
          uVar1 = uVar15 + iVar12;
          uVar15 = uVar15 + 1;
          (&DAT_0018e000)[uVar1] = (&DAT_0018e000)[uVar8];
        } while (uVar15 != uVar16);
        uVar14 = uVar14 + uVar17;
        if (uVar14 != 0x8000) goto LAB_0010a816;
LAB_0010a884:
        DAT_001df800 = 0x8000;
        FUN_001092e0();
        uVar9 = 0;
        if (uVar18 == 0) goto LAB_0010a89a;
      }
      uVar17 = 0x8000 - uVar14;
      if (uVar18 < 0x8000 - uVar14) {
        uVar17 = uVar18;
      }
      uVar18 = uVar18 - uVar17;
      if (uVar14 <= uVar15) goto LAB_0010a7cd;
      if (uVar14 - uVar15 < uVar17) goto LAB_0010a850;
LAB_0010a7d8:
      uVar16 = uVar15 + uVar17;
      uVar8 = 0x10000;
      if (0xffff < uVar9) {
        uVar8 = uVar9;
      }
      __memcpy_chk(&DAT_0018e000 + uVar9,uVar15 + 0x18e000,uVar17,uVar8 - uVar9);
      uVar14 = uVar14 + uVar17;
      if (uVar14 == 0x8000) goto LAB_0010a884;
LAB_0010a816:
      uVar9 = (ulong)uVar14;
    } while (uVar18 != 0);
LAB_0010a89a:
    uVar16 = (uint)uVar9;
  } while( true );
}

