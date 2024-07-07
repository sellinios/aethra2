sudo microk8s kubectl get nodes
sudo microk8s kubectl config view --raw > $HOME/.kube/config
sudo usermod -a -G microk8s sellinios
sudo microk8s enable dns
microk8s kubectl create token default
microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
