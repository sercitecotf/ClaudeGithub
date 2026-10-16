
int FUN_0010a9e0(void)

{
  void *pvVar1;
  long lVar2;
  int iVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  long in_FS_OFFSET;
  undefined4 local_4d0;
  undefined4 local_4cc;
  long local_4c8;
  long local_4c0;
  undefined8 local_4b8 [128];
  undefined8 local_b8 [17];
  long local_30;
  
  local_30 = *(long *)(in_FS_OFFSET + 0x28);
  puVar5 = local_4b8;
  do {
    *puVar5 = 0x800000008;
    puVar5[1] = 0x800000008;
    puVar4 = puVar5 + 4;
    puVar5[2] = 0x800000008;
    puVar5[3] = 0x800000008;
    puVar5 = puVar4;
  } while (puVar4 != local_4b8 + 0x48);
  do {
    *puVar4 = 0x900000009;
    puVar4[1] = 0x900000009;
    puVar5 = puVar4 + 4;
    puVar4[2] = 0x900000009;
    puVar4[3] = 0x900000009;
    puVar4 = puVar5;
  } while (puVar5 != local_b8);
  puVar5 = local_4b8;
  do {
    puVar5[0x80] = 0x700000007;
    puVar5[0x81] = 0x700000007;
    puVar4 = puVar5 + 4;
    puVar5[0x82] = 0x700000007;
    puVar5[0x83] = 0x700000007;
    puVar5 = puVar4;
  } while (local_4b8 + 0xc != puVar4);
  local_b8[0xc] = 0x800000008;
  local_b8[0xd] = 0x800000008;
  local_b8[0xe] = 0x800000008;
  local_b8[0xf] = 0x800000008;
  local_4cc = 7;
  iVar3 = FUN_00105680(local_4b8,0x120,0x101,&DAT_00117240,&DAT_00117200,&local_4c0,&local_4cc);
  if (iVar3 == 0) {
    local_4b8[0] = 0x500000005;
    for (puVar5 = local_4b8 + 1; local_4b8 + 0xf != puVar5; puVar5 = puVar5 + 2) {
      *puVar5 = 0x500000005;
      puVar5[1] = 0x500000005;
    }
    local_4d0 = 5;
    iVar3 = FUN_00105680(local_4b8,0x1e,0,&DAT_001171c0,&DAT_00117180,&local_4c8,&local_4d0);
    if (iVar3 < 2) {
      iVar3 = FUN_0010a3a0(local_4c0,local_4c8,local_4cc,local_4d0);
      if (iVar3 == 0) {
        while (local_4c0 != 0) {
          pvVar1 = (void *)(local_4c0 + -0x10);
          local_4c0 = *(long *)(local_4c0 + -8);
          free(pvVar1);
        }
        iVar3 = 0;
        lVar2 = local_4c8;
        while (lVar2 != 0) {
          pvVar1 = (void *)(lVar2 + -0x10);
          lVar2 = *(long *)(lVar2 + -8);
          free(pvVar1);
        }
      }
      else {
        iVar3 = 1;
      }
    }
    else {
      while (local_4c0 != 0) {
        lVar2 = *(long *)(local_4c0 + -8);
        free((void *)(local_4c0 + -0x10));
        local_4c0 = lVar2;
      }
    }
  }
  if (local_30 == *(long *)(in_FS_OFFSET + 0x28)) {
    return iVar3;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

