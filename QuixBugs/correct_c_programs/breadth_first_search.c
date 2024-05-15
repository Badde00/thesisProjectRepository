#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node
{
  char *value;
  struct Node **successors;
  int successorCount;
} Node;

typedef struct QueueNode
{
  Node *node;
  struct QueueNode *next;
} QueueNode;

QueueNode *queueHead = NULL;
QueueNode *queueTail = NULL;

Node **nodesVisited = NULL;
int nodesVisitedCount = 0;

bool isVisited(Node *node)
{
  for (int i = 0; i < nodesVisitedCount; i++)
  {
    if (nodesVisited[i] == node)
    {
      return true;
    }
  }
  return false;
}

void markAsVisited(Node *node)
{
  nodesVisited = realloc(nodesVisited, (nodesVisitedCount + 1) * sizeof(Node *));
  nodesVisited[nodesVisitedCount++] = node;
}

void enqueue(Node *node)
{
  QueueNode *newQueueNode = (QueueNode *)malloc(sizeof(QueueNode));
  newQueueNode->node = node;
  newQueueNode->next = NULL;
  if (queueTail != NULL)
  {
    queueTail->next = newQueueNode;
  }
  queueTail = newQueueNode;
  if (queueHead == NULL)
  {
    queueHead = newQueueNode;
  }
}

Node *dequeue()
{
  if (queueHead == NULL)
    return NULL;
  QueueNode *temp = queueHead;
  Node *node = temp->node;
  queueHead = queueHead->next;
  if (queueHead == NULL)
  {
    queueTail = NULL;
  }
  free(temp);
  return node;
}

bool breadth_first_search(Node *startNode, Node *goalNode)
{
  enqueue(startNode);
  markAsVisited(startNode);

  while (true)
  {
    Node *node = dequeue();

    if (node == goalNode)
    {
      return true;
    }
    else
    {
      for (int i = 0; i < node->successorCount; i++)
      {
        if (!isVisited(node->successors[i]))
        {
          enqueue(node->successors[i]);
          markAsVisited(node->successors[i]);
        }
      }
    }
  }

  return false;
}
