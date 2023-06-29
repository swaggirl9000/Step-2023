//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head[7];
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//
// return index of the fast bin corresponding to the given size
int get_index(size_t size){
  int bin_index = 0;
  size_t bin_size = 64;

  while (bin_size < size) {
    bin_index++;
    bin_size *= 2;
  }
  return bin_index;
}

void my_add_to_free_list(my_metadata_t *metadata, int bin_index) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head[bin_index];
  my_heap.free_head[bin_index] = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head[bin_index] = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < 7; i++){
    my_heap.free_head[i] = &my_heap.dummy;
  }
    my_heap.dummy.size = 0;
    my_heap.dummy.next = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  int bin_index = get_index(size);
  my_metadata_t *metadata = my_heap.free_head[bin_index];
  my_metadata_t *prev = NULL;
  my_metadata_t *best_prev = NULL;
  my_metadata_t *best_fit = NULL; // best_fit slot variable

// BEST FIT
  while (metadata) {
    if (metadata->size >= size) {
      if (!best_fit || metadata->size < best_fit->size){
        best_fit = metadata;
        best_prev = prev;
      }
    }
    prev = metadata;
    metadata = metadata->next;
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!best_fit) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata, bin_index);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = best_fit + 1;
  size_t remaining_size = best_fit->size - size;
  best_fit->size = size;
  // Remove the free slot from the free list.
  int bin_index = get_index(size);
  my_remove_from_free_list(best_fit, best_prev, bin_index);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata, bin_index);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  int bin_index = get_index(metadata->size);
  my_add_to_free_list(metadata, bin_index);
  // Add the free slot to the free list.
  // my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
