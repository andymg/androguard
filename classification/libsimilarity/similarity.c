/* 
 This file is part of Androguard.

 Copyright (C) 2010, Anthony Desnos <desnos at t0t0.org>
 All rights reserved.

 Androguard is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Androguard is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of  
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with Androguard.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <stdio.h>
#include <string.h>

#include "./z/z.h"
#include "./bz2/bz2.h"
#include "./smaz/smaz.h"
#include "./lzma/lzma.h"
#include "./xz/xz.h"

#define TYPE_Z          0
#define TYPE_BZ2        1
#define TYPE_SMAZ       2
#define TYPE_LZMA       3
#define TYPE_XZ         4

#define M_BLOCK         1000000

unsigned char inbuf[M_BLOCK];
int (*generic_Compress)(int, void *, unsigned int, void *, unsigned int *) = zCompress;

void set_compress_type(int type) {
   if (type == TYPE_Z) {
      generic_Compress = zCompress;
   } else if (type == TYPE_BZ2) {
      generic_Compress = bz2Compress;
   } else if (type == TYPE_SMAZ) {
      generic_Compress = sCompress;
   } else if (type == TYPE_LZMA) {
      generic_Compress = lzmaCompress;
   } else if (type == TYPE_XZ) {
      generic_Compress = xzCompress;
   }
}

struct libsimilarity {
   void *orig;
   unsigned int size_orig;
   void *cmp;
   unsigned size_cmp;

   unsigned int *corig;
   unsigned int *ccmp;
};

typedef struct libsimilarity libsimilarity_t;

unsigned int compress(int level, void *orig, unsigned int size_orig) {
   unsigned int s1, ret;

   ret = generic_Compress( level, orig, size_orig, inbuf, &s1 );
   if (ret < 0) {

   }

   return s1;
}

float ncd(int level, libsimilarity_t *n) 
{
   unsigned int s1, s2, s3, size_join_buff, max, min, ret;
   void *joinbuff;

   //printf("ORIG = 0x%x SIZE_ORIG = 0x%x CMP = 0x%x SIZE_CMP = 0x%x 0x%x 0x%x\n", (unsigned int)(n->orig), n->size_orig, (unsigned int)(n->cmp), n->size_cmp, *(n->corig), *(n->ccmp));

   s1 = *(n->corig);
   if (s1 == 0) {
      s1 = sizeof(inbuf);
      ret = generic_Compress(level, n->orig, n->size_orig, inbuf, &s1);
      //printf("RET = %d AVAIL OUT %d\n", ret, s1);
      if (ret < 0) {
      }

      *(n->corig) = s1;
   }

   s2 = *(n->ccmp);
   if (s2 == 0) {
      s2 = sizeof(inbuf);
      ret = generic_Compress(level, n->cmp, n->size_cmp, inbuf, &s2);
      //printf("RET = %d AVAIL OUT %d\n", ret, s2);
      if (ret < 0) {
      }
      *(n->ccmp) = s2;
   }

   size_join_buff = n->size_orig + n->size_cmp;
   joinbuff = (void *)malloc( size_join_buff );
   if (joinbuff == NULL) {
   }

   memcpy(joinbuff, n->orig, n->size_orig);
   memcpy(joinbuff+n->size_orig, n->cmp, n->size_cmp);

   s3 = sizeof(inbuf);
   ret = generic_Compress(level, joinbuff, size_join_buff, inbuf, &s3);
   free(joinbuff);

   //printf("RET = %d %d AVAIL OUT %d\n", ret, size_join_buff, s3);
   if (ret < 0) {
   }

   max = s1;
   min = s2;
   if (s2 > s1) {
      max = s2;
      min = s1;
   }

   return (float)(s3 - min) / max;
}

float ncs(int level, libsimilarity_t *n) {
   return 1 - ncd( level, n );
}

float cmid(int level, libsimilarity_t *n) {
   unsigned int s1, s2, s3, size_join_buff, max, min, ret;
   void *joinbuff;

   //printf("ORIG = 0x%x SIZE_ORIG = 0x%x CMP = 0x%x SIZE_CMP = 0x%x 0x%x 0x%x\n", (unsigned int)(n->orig), n->size_orig, (unsigned int)(n->cmp), n->size_cmp, *(n->corig), *(n->ccmp));

   s1 = *(n->corig);
   if (s1 == 0) {
      s1 = sizeof(inbuf);
      ret = generic_Compress(level, n->orig, n->size_orig, inbuf, &s1);
      //printf("RET = %d AVAIL OUT %d\n", ret, s1);
      if (ret < 0) {
      }

      *(n->corig) = s1;
   }

   s2 = *(n->ccmp);
   if (s2 == 0) {
      s2 = sizeof(inbuf);
      ret = generic_Compress(level, n->cmp, n->size_cmp, inbuf, &s2);
      //printf("RET = %d AVAIL OUT %d\n", ret, s2);
      if (ret < 0) {
      }
      *(n->ccmp) = s2;
   }

   size_join_buff = n->size_orig + n->size_cmp;
   joinbuff = (void *)malloc( size_join_buff );
   if (joinbuff == NULL) {
   }

   memcpy(joinbuff, n->orig, n->size_orig);
   memcpy(joinbuff+n->size_orig, n->cmp, n->size_cmp);

   s3 = sizeof(inbuf);
   ret = generic_Compress(level, joinbuff, size_join_buff, inbuf, &s3);
   free(joinbuff);

   //printf("RET = %d %d AVAIL OUT %d\n", ret, size_join_buff, s3);
   if (ret < 0) {
   }

   max = s1;
   min = s2;
   if (s2 > s1) {
      max = s2;
      min = s1;
   }

   return (float)(s1 + s2 - s3)/min;
}
