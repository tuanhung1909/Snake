using namespace std;

struct Node {
    int number; 
    bool eliminated; 
    Node *next; 
};

Node *createNode(int number) {
    Node *newNode = new Node;
    newNode->number = number;
    newNode->eliminated = false;
    newNode->next = nullptr;
    return newNode;
}


void insertNode(Node *&head, Node *newNode) {
    if (!head) {
        head = newNode;
        newNode->next = head; 
    } else {
        Node *current = head;
        while (current->next != head) {
            current = current->next;
        }
        current->next = newNode;
        newNode->next = head;
    }
}

Node *findWinner(Node *head, int M) {
    if (!head) {
        return nullptr;
    }

    Node *runner = head;
    while (true) {
        for (int i = 0; i < M - 1; i++) {
            runner = runner->next;
        }
        runner->eliminated = true;
        runner = runner->next;
        int remainingPlayers = 0;
        Node *temp = head;
        while (temp) {
            if (!temp->eliminated) {
                remainingPlayers++;
            }
            temp = temp->next;
        }

        if (remainingPlayers == 1) {
            return runner;
        }
    }
}

int main() {
    int N; 
    int M; 

    cout << "So nguoi choi: ";
    cin >> N;
    if (N <= 0) {
        cout << "So khong hop le" << endl;
        return 1;
    }

    cout << "Nhap khoang dem (M): ";
    cin >> M;
    if (M <= 0) {
        cout << "Khoang khong hop le" << endl;
        return 1;
    }

    Node *head = nullptr;
    for (int i = 1; i <= N; i++) {
        insertNode(head, createNode(i));
    }

    Node *winner = findWinner(head, M);
    if (winner) {
        cout << "nguoi thang la " << winner->number << "!" << endl;
    } else {
        cout << "khong co nguoi thang" << endl;
    }

    Node *current = head;
    while (current) {
        Node *next = current->next;
        delete current;
        current = next;
    }

    return 0;
}